"""Structured report generation from audit results."""

from datetime import datetime
from engine import AuditResult, Severity


def generate_report(audit: AuditResult) -> str:
    """Generate a comprehensive Markdown audit report."""
    lines = [
        f"# SEO Audit Report: {audit.url}",
        f"**Date:** {audit.timestamp}",
        f"**Pages crawled:** {audit.pages_crawled}",
        "",
        "---",
        "",
        f"## Overall SEO Health Score: {audit.overall_score}/100",
        "",
    ]

    # Score bar visualization
    filled = int(audit.overall_score / 5)
    bar = "█" * filled + "░" * (20 - filled)
    lines.append(f"`[{bar}]` {audit.overall_score}/100")
    lines.append("")

    # Category breakdown
    lines.append("## Category Breakdown")
    lines.append("")
    lines.append("| Category | Score | Status |")
    lines.append("|----------|-------|--------|")
    for cs in audit.categories:
        status = "✅" if cs.score >= 80 else ("⚠️" if cs.score >= 50 else "❌")
        bar = "█" * int(cs.score / 10) + "░" * (10 - int(cs.score / 10))
        lines.append(f"| {cs.category.title()} ({int(cs.weight*100)}%) | {cs.score}/100 `{bar}` | {status} |")
    lines.append("")

    # Comparison with previous
    if audit.comparison:
        comp = audit.comparison
        delta = comp.get("score_delta", 0)
        arrow = "↑" if delta > 0 else ("↓" if delta < 0 else "→")
        lines.append(f"## Comparison with Previous Audit")
        lines.append(f"**Overall:** {arrow} {delta:+.1f} points (was {comp.get('previous_score', 'N/A')} on {comp.get('previous_date', 'N/A')})")
        lines.append("")
        cat_deltas = comp.get("category_deltas", {})
        for cat, d in cat_deltas.items():
            if d != 0:
                arr = "↑" if d > 0 else "↓"
                lines.append(f"- **{cat.title()}:** {arr} {d:+.1f}")
        new_issues = comp.get("new_issues", [])
        resolved = comp.get("resolved_issues", [])
        if new_issues:
            lines.append(f"\n**New issues:** {len(new_issues)}")
            for i in new_issues[:10]:
                lines.append(f"- `{i}`")
        if resolved:
            lines.append(f"\n**Resolved issues:** {len(resolved)}")
            for i in resolved[:10]:
                lines.append(f"- ~~`{i}`~~")
        lines.append("")

    # CWV data
    if audit.cwv_data and audit.cwv_data.source != "none":
        cwv = audit.cwv_data
        lines.append("## Core Web Vitals")
        lines.append(f"*Source: {cwv.source} data*")
        lines.append("")
        lines.append("| Metric | Value | Rating |")
        lines.append("|--------|-------|--------|")
        if cwv.lcp_ms is not None:
            lines.append(f"| LCP | {cwv.lcp_ms:.0f}ms | {_rating_emoji(cwv.lcp_rating)} {cwv.lcp_rating} |")
        if cwv.inp_ms is not None:
            lines.append(f"| INP | {cwv.inp_ms:.0f}ms | {_rating_emoji(cwv.inp_rating)} {cwv.inp_rating} |")
        if cwv.cls is not None:
            lines.append(f"| CLS | {cwv.cls:.3f} | {_rating_emoji(cwv.cls_rating)} {cwv.cls_rating} |")
        lines.append("")

        if cwv.lighthouse_performance is not None:
            lines.append("### Lighthouse Scores")
            lines.append(f"- Performance: {cwv.lighthouse_performance}/100")
            if cwv.lighthouse_accessibility is not None:
                lines.append(f"- Accessibility: {cwv.lighthouse_accessibility}/100")
            if cwv.lighthouse_seo is not None:
                lines.append(f"- SEO: {cwv.lighthouse_seo}/100")
            lines.append("")

        if cwv.opportunities:
            lines.append("### Top Opportunities")
            for opp in cwv.opportunities[:5]:
                lines.append(f"- **{opp['title']}** — est. {opp['savings_ms']}ms savings")
            lines.append("")

    # GSC data
    if audit.search_data and audit.search_data.source != "none":
        sd = audit.search_data
        lines.append("## Google Search Console Data")
        lines.append(f"*Date range: {sd.date_range}*")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Total Impressions | {sd.total_impressions:,} |")
        lines.append(f"| Total Clicks | {sd.total_clicks:,} |")
        if sd.avg_position is not None:
            lines.append(f"| Avg Position | {sd.avg_position:.1f} |")
        if sd.avg_ctr is not None:
            lines.append(f"| Avg CTR | {sd.avg_ctr:.1%} |")
        lines.append(f"| Indexed Pages | {sd.indexed_pages} |")
        if sd.impressions_trend is not None:
            trend_emoji = "📈" if sd.impressions_trend >= 1.0 else "📉"
            lines.append(f"| Impressions Trend | {trend_emoji} {sd.impressions_trend:.0%} vs previous period |")
        lines.append("")

        if sd.declining_pages:
            lines.append(f"### Declining Pages ({len(sd.declining_pages)})")
            for page_url in sd.declining_pages[:10]:
                lines.append(f"- {page_url}")
            if len(sd.declining_pages) > 10:
                lines.append(f"- ... and {len(sd.declining_pages) - 10} more")
            lines.append("")

    # Issues by severity
    for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
        sev_issues = [i for i in audit.issues if i.severity == sev and not i.passed]
        if sev_issues:
            emoji = {"critical": "🛑", "high": "🔴", "medium": "🟡", "low": "🔵"}.get(sev.value, "")
            label = {"critical": "Critical (fix immediately)",
                     "high": "High Priority (fix within 1 week)",
                     "medium": "Medium Priority (fix within 1 month)",
                     "low": "Low Priority (backlog)"}.get(sev.value, sev.value)
            lines.append(f"## {emoji} {label}")
            lines.append("")
            for issue in sev_issues:
                lines.append(f"- **`{issue.check_id}`** — {issue.message}")
            lines.append("")

    # Fixes
    if audit.fixes:
        lines.append("## Auto-Generated Fixes")
        lines.append("")
        for fix in audit.fixes:
            lines.append(f"### {fix.description}")
            lines.append(f"*Impact: {fix.impact}*")
            lines.append(f"```\n{fix.code}\n```")
            if fix.apply_command:
                lines.append(f"Apply: `{fix.apply_command}`")
            lines.append("")

    lines.append("---")
    lines.append(f"*Generated by Claude SEO v2 — {datetime.now().isoformat()}*")

    return "\n".join(lines)


def _rating_emoji(rating: str) -> str:
    return {"good": "✅", "needs-improvement": "⚠️", "poor": "❌"}.get(rating, "❓")
