# Claude SEO v2 — Deterministic SEO Engine

## Project Overview

Claude SEO v2 is a deterministic SEO analysis engine for Claude Code.
98 atomic checks (7 categories) with traceable formulas. Async multi-page crawler.
Real CWV via PageSpeed Insights. Optional GSC integration for real search data.
Internal link graph with PageRank. Auto-fix generation. Audit history with
regression detection. CI/CD.

## Architecture

```
claude-seo/
  CLAUDE.md                          # This file
  .claude-plugin/plugin.json         # Plugin manifest (v2.0.0)
  engine/                            # Deterministic measurement engine
    __init__.py                      # Core data models
    crawler.py                       # Async multi-page spider
    scorer.py                        # 98-check scoring engine
    link_graph.py                    # PageRank + cannibalization
    auto_fixer.py                    # Ready-to-apply fix generation
    db.py                            # SQLite audit history
    report.py                        # Markdown report generation
    cli.py                           # CLI entry point
  integrations/                      # External data sources
    pagespeed.py                     # Google PageSpeed Insights API
    gsc.py                           # Google Search Console (optional)
  seo/                               # Main orchestrator skill
    SKILL.md                         # Entry point + routing
    references/                      # Knowledge base (from v1)
  skills/                            # 16 specialized sub-skills
    seo-audit/SKILL.md              # Engine-powered full audit
    seo-fix/SKILL.md                # Auto-fix generation (NEW)
    seo-linkgraph/SKILL.md          # Link graph analysis (NEW)
    seo-monitor/SKILL.md            # Regression tracking (NEW)
    seo-logfile/SKILL.md            # Server log analysis (NEW)
    seo-technical/SKILL.md          # Technical SEO
    seo-content/SKILL.md            # E-E-A-T and content
    seo-schema/SKILL.md             # Schema detection/generation
    seo-sitemap/SKILL.md            # Sitemap analysis
    seo-images/SKILL.md             # Image optimization
    seo-geo/SKILL.md                # AI search / GEO
    seo-page/SKILL.md               # Single-page analysis
    seo-plan/SKILL.md               # Strategic planning
    seo-programmatic/SKILL.md       # Programmatic SEO
    seo-competitor-pages/SKILL.md   # Competitor comparison
    seo-hreflang/SKILL.md           # International SEO
  agents/                            # 7 parallel subagents
  hooks/                             # Pre-commit + regression hooks
  ci/                                # GitHub Actions + GitLab CI
  schema/                            # JSON-LD templates
  tests/                             # Test suite
```

## Development Rules

- Keep SKILL.md files under 500 lines / 5000 tokens
- Reference files: focused, under 200 lines
- Engine modules: full docstrings, type hints, error handling
- All scoring must be deterministic — same input → same output
- Every CheckResult must include evidence dict with raw data
- Tests: fixtures with expected scores for regression testing
- Agents via Task tool with `context: fork`, never Bash
- Python deps: `~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0/.venv/`

## Key Principles

1. **Deterministic**: Every score computed from formulas, not hallucinated
2. **Measurable**: Real CWV via PageSpeed, real search data via GSC, real link graph from crawl
3. **Actionable**: Every issue comes with a ready-to-apply fix
4. **Traceable**: Every score linked to evidence data
5. **Progressive**: Engine degrades gracefully when deps missing
6. **Historical**: Audit history enables regression detection
