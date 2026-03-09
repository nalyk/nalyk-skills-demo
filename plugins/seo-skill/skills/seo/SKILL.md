---
name: seo
description: >
  Comprehensive deterministic SEO analysis for any website. Performs full site
  audits with async multi-page crawling (up to 500 pages), reproducible scoring
  (98 atomic checks), real Core Web Vitals via PageSpeed Insights API, optional
  Google Search Console integration for real search data, internal
  link graph analysis with PageRank, auto-fix generation, E-E-A-T assessment
  (Dec 2025 update), schema validation, GEO optimization for AI Overviews/
  ChatGPT/Perplexity, audit history with regression detection, and CI/CD
  integration. Industry detection for SaaS, e-commerce, local, publishers,
  agencies. Triggers on: "SEO", "audit", "schema", "Core Web Vitals",
  "sitemap", "E-E-A-T", "AI Overviews", "GEO", "technical SEO".
---

# SEO v2 — Deterministic SEO Analysis Engine

Comprehensive SEO analysis with **reproducible scoring**. Every score
computed from 98 atomic checks with traceable formulas. Same URL → same
score, every time. Orchestrates 16 sub-skills and 7 subagents.

## Engine Execution

The Python engine lives at `~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0/engine/`. To run it:

```bash
# Full audit via CLI (preferred — handles all steps automatically)
cd ~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0 && .venv/bin/python -m engine.cli audit <URL> --output report.md

# With PageSpeed API key for real CWV data
cd ~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0 && PAGESPEED_API_KEY="your-key" .venv/bin/python -m engine.cli audit <URL> --compare --output report.md

# With GSC credentials for real search data
cd ~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0 && .venv/bin/python -m engine.cli audit <URL> --gsc-credentials /path/to/gsc-sa.json --output report.md

# View audit history
cd ~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0 && .venv/bin/python -m engine.cli history <URL>

# If venv doesn't exist, use system Python (requires: pip install beautifulsoup4 requests lxml)
cd ~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0 && python3 -m engine.cli audit <URL>
```

For programmatic use from other agents/skills:
```bash
cd ~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0 && .venv/bin/python -c "
from engine.cli import run_audit
audit = run_audit('$URL', max_pages=200, compare=True, output='report.md')
print(f'Score: {audit.overall_score}/100')
"
```

**Requirements**: `beautifulsoup4`, `requests`, `lxml` (core); `aiohttp` (optional async);
`google-api-python-client`, `google-auth`, `google-auth-oauthlib` (optional GSC).
All installed in `.venv/` by `install.sh`. Engine degrades gracefully if deps are missing.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo audit <url>` | Full site audit: crawl + score + CWV + fixes |
| `/seo audit <url> --compare` | Audit with regression detection |
| `/seo page <url>` | Deep single-page analysis |
| `/seo fix <url>` | Generate ready-to-apply fixes |
| `/seo fix <url> --apply` | Auto-apply fixes to local project |
| `/seo linkgraph <url>` | Internal link graph + PageRank analysis |
| `/seo cwv <url>` | Real Core Web Vitals from PageSpeed API |
| `/seo history <url>` | Show audit score history over time |
| `/seo monitor <url>` | Set up CI/CD monitoring |
| `/seo technical <url>` | Technical SEO audit (9 categories) |
| `/seo content <url>` | E-E-A-T and content quality analysis |
| `/seo schema <url>` | Detect, validate, and generate Schema.org |
| `/seo sitemap <url or generate>` | Analyze or generate XML sitemaps |
| `/seo images <url>` | Image optimization analysis |
| `/seo geo <url>` | AI search / GEO optimization |
| `/seo plan <business-type>` | Strategic SEO planning |
| `/seo programmatic [url\|plan]` | Programmatic SEO analysis |
| `/seo competitor-pages [url\|generate]` | Competitor comparison pages |
| `/seo hreflang [url]` | Hreflang/i18n audit and generation |
| `/seo logfile <path>` | Crawl log analysis |
| `/seo export <url> --format json` | Export audit data |
| `/seo dataforseo [command]` | Live data via DataForSEO (extension) |

## How the Engine Works

### Step 1: Crawl
Async spider (`engine/crawler.py`) fetches up to 500 pages with:
- BFS traversal, robots.txt obedience, SSRF protection
- Link extraction, redirect chain tracking, broken link detection
- Schema/meta/heading/image extraction per page
- Content fingerprinting for duplicate detection
- Sitemap parsing and orphan page detection

### Step 2: Measure CWV
`integrations/pagespeed.py` calls Google PageSpeed Insights API (free):
- Field data (CrUX): real user LCP, INP, CLS at 75th percentile
- Lab data (Lighthouse): performance, accessibility, SEO scores
- Specific optimization opportunities with estimated savings

### Step 3: Score Deterministically
`engine/scorer.py` runs 98 registered checks, each returning:
- score: 0.0 to 1.0 (computed, not hallucinated)
- passed: boolean
- evidence: raw data supporting the finding

Formula: `category_score = Σ(check.score × check.weight) / Σ(check.weight) × 100`
Overall: `Σ(category.score × category.weight)`

### Step 4: Generate Fixes
`engine/auto_fixer.py` produces ready-to-apply patches:
- Missing meta tags → generated from page content
- Missing schema → JSON-LD from actual page data
- Security headers → Nginx/Apache/Cloudflare configs
- Missing llms.txt → generated from site structure
- Missing alt text → descriptive text from image context

### Step 5: Compare & Store
`engine/db.py` stores audit in SQLite history:
- Score trends over time
- Regression detection (new issues, resolved issues)
- CI/CD integration for merge-blocking

## Scoring Weights

| Category | Weight | Checks |
|----------|--------|--------|
| Technical SEO | 25% | 29 checks (incl. 2 GSC) |
| Content Quality | 25% | 16 checks |
| On-Page SEO | 20% | 18 checks (incl. 4 GSC) |
| Schema / Structured Data | 10% | 10 checks |
| Performance (CWV) | 10% | 9 checks |
| Images | 5% | 7 checks |
| AI Search Readiness | 5% | 9 checks |

## Industry Detection

Detect business type from homepage signals:
- **SaaS**: pricing page, /features, /integrations, "free trial"
- **Local Service**: phone, address, service area, Google Maps embed
- **E-commerce**: /products, /cart, "add to cart", product schema
- **Publisher**: /blog, /articles, article schema, author pages
- **Agency**: /case-studies, /portfolio, client logos

## Quality Gates

Read `references/quality-gates.md` for thin content thresholds.
Hard rules:
- ⚠️ WARNING at 30+ location pages (enforce 60%+ unique content)
- 🛑 HARD STOP at 50+ location pages (require justification)
- Never recommend HowTo schema (deprecated Sept 2023)
- FAQ schema only for government and healthcare sites
- All CWV references use INP, never FID

## Reference Files

Load on-demand — do NOT load all at startup:
- `references/cwv-thresholds.md` — Current CWV thresholds
- `references/schema-types.md` — Supported types with deprecation status
- `references/eeat-framework.md` — E-E-A-T criteria (Sept 2025 QRG + Dec 2025)
- `references/quality-gates.md` — Content length minimums, uniqueness thresholds

## Sub-Skills (16)

1. **seo-audit** — Full website audit with engine
2. **seo-page** — Deep single-page analysis
3. **seo-technical** — Technical SEO (9 categories)
4. **seo-content** — E-E-A-T and content quality
5. **seo-schema** — Schema detection and generation
6. **seo-images** — Image optimization
7. **seo-sitemap** — Sitemap analysis and generation
8. **seo-geo** — AI search / GEO optimization
9. **seo-plan** — Strategic planning with templates
10. **seo-programmatic** — Programmatic SEO analysis
11. **seo-competitor-pages** — Competitor comparison pages
12. **seo-hreflang** — Hreflang/i18n audit
13. **seo-fix** — Auto-fix generation and application
14. **seo-linkgraph** — Internal link graph analysis
15. **seo-monitor** — Regression tracking and CI/CD
16. **seo-logfile** — Server log analysis for crawl insights

## Subagents (7)

- `seo-technical` — Crawlability, indexability, security, CWV
- `seo-content` — E-E-A-T, readability, thin content
- `seo-schema` — Detection, validation, generation
- `seo-sitemap` — Structure, coverage, quality gates
- `seo-performance` — Core Web Vitals measurement
- `seo-visual` — Screenshots, mobile testing
- `seo-linkgraph` — Internal link graph + PageRank

## Routing Logic

When the user invokes `/seo <command>`, route to the appropriate sub-skill:

| User says | Load sub-skill | Then run |
|-----------|---------------|----------|
| `/seo audit <url>` | `seo-audit` | Engine CLI: `cd ~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0 && .venv/bin/python -m engine.cli audit <url> --compare --output report.md` |
| `/seo page <url>` | `seo-page` | Fetch single page, run scorer checks |
| `/seo fix <url>` | `seo-fix` | Run audit first, then auto-fixer |
| `/seo linkgraph <url>` | `seo-linkgraph` | Run crawl, then link_graph.py |
| `/seo cwv <url>` | `seo-audit` | Run with PageSpeed only |
| `/seo history <url>` | `seo-monitor` | `cd ~/.claude/plugins/cache/nalyk-skills-demo/seo-skill/2.2.0 && .venv/bin/python -m engine.cli history <url>` |
| `/seo monitor <url>` | `seo-monitor` | Set up CI/CD config |
| `/seo technical <url>` | `seo-technical` | Technical analysis |
| `/seo content <url>` | `seo-content` | E-E-A-T analysis |
| `/seo schema <url>` | `seo-schema` | Schema detection/generation |
| `/seo sitemap <url>` | `seo-sitemap` | Sitemap analysis |
| `/seo images <url>` | `seo-images` | Image optimization |
| `/seo geo <url>` | `seo-geo` | AI search optimization |
| `/seo plan <type>` | `seo-plan` | Strategic planning |
| `/seo programmatic` | `seo-programmatic` | Programmatic SEO |
| `/seo competitor-pages` | `seo-competitor-pages` | Competitor analysis |
| `/seo hreflang <url>` | `seo-hreflang` | International SEO |
| `/seo logfile <path>` | `seo-logfile` | Server log analysis |

For **autonomous/agentic use** (no human in loop):
1. Run the CLI command above — it outputs a structured Markdown report
2. Parse the JSON output (`--output audit.json`) for programmatic decisions
3. Use `--fail-on-regression` for CI/CD gating (exit code 1 = regression)

For **parallel subagent dispatch** (Claude Code):
Launch subagents using `Task(subagent_type="general-purpose")` with the agent
definitions from `~/.claude/agents/seo-*.md`. Each agent has its own tool
permissions and specialization. Run up to 7 in parallel for full-site analysis.
