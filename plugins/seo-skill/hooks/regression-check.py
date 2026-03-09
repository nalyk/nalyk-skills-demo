#!/usr/bin/env python3
"""Post-audit regression check hook.

Compares current audit with last stored audit.
Returns exit code 2 if critical regressions detected.

Hook configuration in ~/.claude/settings.json:
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0/hooks/regression-check.py",
            "exitCodes": { "2": "block" }
          }
        ]
      }
    ]
  }
}
"""

import json
import sys
import os

sys.path.insert(0, os.path.expanduser("~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0"))

try:
    from engine.db import AuditDB
except ImportError:
    sys.exit(0)  # Engine not installed, skip


def main():
    db = AuditDB()

    # Check for recent audit results in working directory
    for f in ["audit-report.json", "FULL-AUDIT-REPORT.json"]:
        if os.path.exists(f):
            with open(f) as fh:
                data = json.load(fh)
            url = data.get("url")
            if not url:
                continue

            previous = db.get_previous(url)
            if not previous:
                print("✓ First audit — no regression check needed")
                sys.exit(0)

            current_score = data.get("overall_score", 0)
            prev_score = previous.get("overall_score", 0)
            delta = current_score - prev_score

            if delta < -5:
                print(f"🛑 REGRESSION: Score dropped {delta:.1f} points ({prev_score:.1f} → {current_score:.1f})")
                print("   Review new issues before proceeding.")
                sys.exit(2)
            elif delta < 0:
                print(f"⚠️  Minor regression: {delta:+.1f} points")
                sys.exit(0)
            else:
                print(f"✓ Score improved: {delta:+.1f} points")
                sys.exit(0)

    # No audit file found
    sys.exit(0)


if __name__ == "__main__":
    main()
