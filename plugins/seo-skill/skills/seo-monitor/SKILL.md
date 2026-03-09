---
name: seo-monitor
description: >
  SEO regression tracking and CI/CD integration. Store audit history in SQLite,
  compare scores over time, detect regressions, and integrate with GitHub
  Actions / GitLab CI for automated SEO checks on PRs. Use when user says
  "monitor SEO", "track SEO", "regression", "CI/CD", "history", or "compare".
---

# SEO Monitoring & Regression Detection

Track SEO health over time and catch regressions before they hit production.

## Commands

| Command | What it does |
|---------|-------------|
| `/seo history <url>` | Show audit score history |
| `/seo audit <url> --compare` | Audit with regression detection |
| `/seo monitor setup` | Generate CI/CD config files |

## Audit History

Stored in SQLite at `~/.claude/seo-audit-history.db`.

### What's Tracked
- Overall score and all category scores
- Every individual check result with evidence
- Pages crawled count
- Timestamps for trend analysis

### Comparison Output
```
📈 Compared with previous audit (2026-02-09):
  Overall: ↑ +4.2 points (68.3 → 72.5)

  Category changes:
  - Technical: ↑ +2.1
  - Content:   ↑ +5.3
  - Schema:    ↑ +8.0
  - CWV:       ↓ -1.2

  New issues (3):
  - tech.url.no_redirect_chains
  - images.alt_text.descriptive
  - geo.llms_txt.exists

  Resolved issues (5):
  - onpage.title.exists
  - schema.no_placeholder
  - tech.security.hsts
  - onpage.meta_desc.exists
  - content.eeat.contact_info
```

## CI/CD Integration

### GitHub Actions
Copy `ci/github-action.yml` to `.github/workflows/seo-audit.yml`.

Triggers:
- On push to main (when HTML/PHP/JSX files change)
- Weekly scheduled run (Monday 6am)
- PR comments with audit summary

### GitLab CI
Copy `ci/gitlab-ci.yml` to your `.gitlab-ci.yml`.

### Merge Blocking
Use `--fail-on-regression` flag to exit with code 1 if score decreased:
```bash
python -m engine.cli audit https://yoursite.com --compare --fail-on-regression
```

## Regression Hook

`hooks/regression-check.py` runs post-audit and:
1. Compares with last stored audit
2. Flags new critical/high issues
3. Reports score deltas per category
4. Returns exit code 2 to block if critical regressions detected
