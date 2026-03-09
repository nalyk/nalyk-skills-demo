"""SQLite-based audit history for regression detection."""

import json
import os
import sqlite3
from datetime import datetime
from typing import Optional

from engine import AuditResult, CategoryScore


DB_PATH = os.path.expanduser("~/.claude/seo-audit-history.db")


class AuditDB:
    """Persistent audit history with regression detection."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    overall_score REAL,
                    tech_score REAL,
                    content_score REAL,
                    onpage_score REAL,
                    schema_score REAL,
                    perf_score REAL,
                    images_score REAL,
                    geo_score REAL,
                    pages_crawled INTEGER,
                    issues_json TEXT,
                    config_json TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS check_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    audit_id INTEGER REFERENCES audits(id),
                    check_id TEXT NOT NULL,
                    score REAL,
                    passed BOOLEAN,
                    evidence_json TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_audits_url ON audits(url)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_checks_audit ON check_history(audit_id)")

    def save_audit(self, audit: AuditResult) -> None:
        """Save audit result to history."""
        cat_map = {cs.category: cs.score for cs in audit.categories}
        issues_json = json.dumps([
            {"check_id": i.check_id, "passed": i.passed, "score": i.score,
             "severity": i.severity.value if hasattr(i.severity, "value") else str(i.severity),
             "message": i.message}
            for i in audit.issues
        ])

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    INSERT INTO audits (url, timestamp, overall_score, tech_score, content_score,
                        onpage_score, schema_score, perf_score, images_score, geo_score,
                        pages_crawled, issues_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    audit.url, audit.timestamp, audit.overall_score,
                    cat_map.get("technical", 0), cat_map.get("content", 0),
                    cat_map.get("onpage", 0), cat_map.get("schema", 0),
                    cat_map.get("performance", 0), cat_map.get("images", 0),
                    cat_map.get("geo", 0), audit.pages_crawled, issues_json,
                ))
                audit_id = cursor.lastrowid

                for issue in audit.issues:
                    conn.execute("""
                        INSERT INTO check_history (audit_id, check_id, score, passed, evidence_json)
                        VALUES (?, ?, ?, ?, ?)
                    """, (audit_id, issue.check_id, issue.score, issue.passed,
                          json.dumps(issue.evidence)))
        except sqlite3.Error as e:
            import sys
            print(f"Warning: Failed to save audit to history: {e}", file=sys.stderr)

    def get_previous(self, url: str) -> Optional[dict]:
        """Get last audit for URL."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM audits WHERE url = ? ORDER BY timestamp DESC LIMIT 1",
                (url,)
            ).fetchone()
            if row:
                return dict(row)
        return None

    def get_history(self, url: str, limit: int = 10) -> list[dict]:
        """Get audit history for URL."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM audits WHERE url = ? ORDER BY timestamp DESC LIMIT ?",
                (url, limit)
            ).fetchall()
            return [dict(r) for r in rows]

    def compare(self, current: AuditResult, previous: dict) -> dict:
        """Compare current audit with previous."""
        cat_map = {cs.category: cs.score for cs in current.categories}
        prev_issues = json.loads(previous.get("issues_json", "[]"))
        prev_check_ids = {i["check_id"] for i in prev_issues if not i.get("passed", True)}
        curr_check_ids = {i.check_id for i in current.issues if not i.passed}

        return {
            "score_delta": round(current.overall_score - (previous.get("overall_score") or 0), 1),
            "category_deltas": {
                "technical": round(cat_map.get("technical", 0) - (previous.get("tech_score") or 0), 1),
                "content": round(cat_map.get("content", 0) - (previous.get("content_score") or 0), 1),
                "onpage": round(cat_map.get("onpage", 0) - (previous.get("onpage_score") or 0), 1),
                "schema": round(cat_map.get("schema", 0) - (previous.get("schema_score") or 0), 1),
                "performance": round(cat_map.get("performance", 0) - (previous.get("perf_score") or 0), 1),
                "images": round(cat_map.get("images", 0) - (previous.get("images_score") or 0), 1),
                "geo": round(cat_map.get("geo", 0) - (previous.get("geo_score") or 0), 1),
            },
            "new_issues": list(curr_check_ids - prev_check_ids),
            "resolved_issues": list(prev_check_ids - curr_check_ids),
            "previous_score": previous.get("overall_score", 0),
            "previous_date": previous.get("timestamp", ""),
        }
