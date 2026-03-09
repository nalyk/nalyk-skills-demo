# Claude SEO v2 — Deterministic SEO Engine

Comprehensive SEO analysis skill for Claude Code with **reproducible, deterministic scoring**. Every score computed from 98 atomic checks with traceable formulas. Same URL → same score, every time.

## What's New in v2

| Feature | v1 | v2 |
|---------|----|----|
| Scoring | Claude guesses a number | 98 deterministic checks with formulas |
| Crawling | 1 page (fetch_page.py) | Async spider, up to 500 pages |
| Core Web Vitals | Guesses from HTML | Real data via PageSpeed Insights API |
| Internal Links | None | PageRank, orphan/dead-end detection |
| Fixes | "Add schema markup" | Actual JSON-LD from your page content |
| History | None | SQLite audit history, regression detection |
| CI/CD | None | GitHub Actions + GitLab CI templates |
| Cannibalization | None | TF-IDF similarity detection |
| Knowledge Base | Excellent (kept) | Preserved and enhanced |

## Installation

```bash
/plugin install seo-skill@nalyk-skills-demo
```

The plugin includes a Python engine. After installation, install Python dependencies:

```bash
cd ~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Optional: set `PAGESPEED_API_KEY` for real Core Web Vitals data (free, 25K queries/day).

## Quick Start

```bash
claude

# Full audit with deterministic scoring
/seo audit https://example.com

# Audit with regression detection
/seo audit https://example.com --compare

# Generate ready-to-apply fixes
/seo fix https://example.com

# Internal link graph analysis
/seo linkgraph https://example.com

# Real Core Web Vitals
/seo cwv https://example.com

# Audit history
/seo history https://example.com
```

## All Commands

| Command | Description |
|---------|-------------|
| `/seo audit <url>` | Full site audit: crawl + score + CWV + fixes |
| `/seo audit <url> --compare` | Audit with regression detection |
| `/seo page <url>` | Deep single-page analysis |
| `/seo fix <url>` | Generate ready-to-apply fixes |
| `/seo linkgraph <url>` | Internal link graph + PageRank |
| `/seo cwv <url>` | Real Core Web Vitals |
| `/seo history <url>` | Audit score history |
| `/seo monitor setup` | Generate CI/CD configs |
| `/seo technical <url>` | Technical SEO audit (9 categories) |
| `/seo content <url>` | E-E-A-T and content quality |
| `/seo schema <url>` | Schema detection, validation, generation |
| `/seo sitemap <url>` | Sitemap analysis and generation |
| `/seo images <url>` | Image optimization |
| `/seo geo <url>` | AI search / GEO optimization |
| `/seo plan <type>` | Strategic SEO planning |
| `/seo programmatic <url>` | Programmatic SEO analysis |
| `/seo competitor-pages <url>` | Competitor comparison pages |
| `/seo hreflang <url>` | International SEO / hreflang |
| `/seo logfile <path>` | Server access log analysis |

## Engine Architecture

```
engine/
├── __init__.py          # Core data models (PageData, CrawlResult, etc.)
├── crawler.py           # Async multi-page spider (aiohttp + requests fallback)
├── scorer.py            # 98-check deterministic scoring engine
├── link_graph.py        # PageRank + cannibalization detection
├── auto_fixer.py        # Ready-to-apply fix generation
├── db.py                # SQLite audit history
├── report.py            # Markdown report generation
└── cli.py               # CLI entry point
```

## Scoring

98 checks across 7 categories, each with a deterministic formula:

| Category | Weight | Checks |
|----------|--------|--------|
| Technical SEO | 25% | 19 |
| Content Quality | 25% | 10 |
| On-Page SEO | 20% | 8 |
| Schema | 10% | 5 |
| Performance (CWV) | 10% | 4 |
| Images | 5% | 4 |
| AI Search / GEO | 5% | 6 |

Every score traceable: `check.score × check.weight` → category → overall.

## CLI Usage (standalone)

```bash
# Run audit from command line
python -m engine.cli audit https://example.com --output report.md

# With PageSpeed API key for real CWV
PAGESPEED_API_KEY=your_key python -m engine.cli audit https://example.com

# Compare with previous
python -m engine.cli audit https://example.com --compare

# CI/CD mode (exit 1 on regression)
python -m engine.cli audit https://example.com --compare --fail-on-regression

# View history
python -m engine.cli history https://example.com
```

## Requirements

- Python 3.10+
- Claude Code CLI
- Optional: Google PageSpeed API key (free, 25K queries/day)

## Tests

```bash
python -m pytest tests/ -v
# or without pytest:
python tests/test_engine.py
```

## License

MIT License — see [LICENSE](LICENSE).

## Credits

v2 built on the excellent knowledge base from [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo). All E-E-A-T frameworks, schema deprecation tracking, GEO statistics, quality gates, and industry templates preserved.
