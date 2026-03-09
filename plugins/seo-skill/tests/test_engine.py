"""Tests for the deterministic scoring engine.

Run: python -m pytest tests/ -v
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import PageData, CrawlResult, CWVData, SearchData
from engine.scorer import ScoringEngine


def _make_page(url="https://example.com", title="Example Page",
               meta_desc="Example description for this page about things",
               canonical=None, h1=None, h2=None, schema_blocks=None,
               images=None, internal_links=None, word_count=500,
               headers=None, html="", meta_robots=None):
    return PageData(
        url=url, final_url=url, status_code=200,
        html=html or f"<html><head><title>{title}</title></head><body>{'word ' * word_count}</body></html>",
        headers=headers or {},
        title=title,
        meta_description=meta_desc,
        meta_robots=meta_robots,
        canonical=canonical or url,
        h1=h1 or [title],
        h2=h2 or ["Section 1", "Section 2"],
        h3=[],
        images=images or [],
        internal_links=internal_links or [{"href": "https://example.com/about", "text": "About"}],
        external_links=[],
        schema_blocks=schema_blocks or [],
        open_graph={"og:title": title, "og:description": meta_desc},
        twitter_card={"twitter:card": "summary"},
        word_count=word_count,
    )


def _make_context(pages=None, robots_txt="User-agent: *\nAllow: /\nSitemap: https://example.com/sitemap.xml",
                  sitemap_urls=None, cwv=None):
    if pages is None:
        pages = {"https://example.com": _make_page()}

    crawl = CrawlResult(
        start_url="https://example.com",
        pages=pages,
        link_graph={url: set() for url in pages},
        sitemap_urls=sitemap_urls or set(pages.keys()),
    )

    return {
        "pages": pages,
        "crawl": crawl,
        "cwv": cwv,
        "robots_txt": robots_txt,
        "sitemap_urls": sitemap_urls or set(pages.keys()),
        "llms_txt": "",
    }


class TestScoringEngine:

    def test_engine_runs_without_error(self):
        engine = ScoringEngine()
        ctx = _make_context()
        overall, categories, issues = engine.run_all(ctx)
        assert isinstance(overall, float)
        assert 0 <= overall <= 100
        assert len(categories) == 7

    def test_perfect_page_scores_high(self):
        page = _make_page(
            url="https://example.com",
            title="Example Business - Professional Services",
            meta_desc="Professional services for businesses. Contact us today for a free consultation.",
            h1=["Example Business - Professional Services"],
            schema_blocks=[{"@context": "https://schema.org", "@type": "Organization", "name": "Example"}],
            images=[{"src": "hero.webp", "alt": "Professional team meeting", "width": "800", "height": "600"}],
            headers={
                "Strict-Transport-Security": "max-age=31536000",
                "Content-Security-Policy": "default-src 'self'",
                "X-Content-Type-Options": "nosniff",
            },
            word_count=1500,
            html='<html><head><meta name="viewport" content="width=device-width"><meta name="robots" content="index,follow"></head><body><span class="author">John Doe</span><time datetime="2026-01-01">Jan 2026</time><a href="mailto:info@example.com">Contact</a><a href="/privacy">Privacy</a>word ' * 500 + '</body></html>',
        )
        ctx = _make_context(
            pages={"https://example.com": page},
            cwv=CWVData(lcp_ms=1800, inp_ms=150, cls=0.05, source="field",
                        lighthouse_performance=92, lighthouse_accessibility=95,
                        lighthouse_seo=100),
        )

        engine = ScoringEngine()
        overall, categories, issues = engine.run_all(ctx)
        assert overall > 60, f"Perfect page should score >60, got {overall}"

    def test_empty_page_scores_low(self):
        page = _make_page(
            title=None, meta_desc=None, canonical=None,
            h1=[], schema_blocks=[], images=[],
            internal_links=[], word_count=50, html="<html><body>short</body></html>",
        )
        ctx = _make_context(pages={"https://example.com": page}, robots_txt="")

        engine = ScoringEngine()
        overall, categories, issues = engine.run_all(ctx)
        assert overall < 50, f"Empty page should score <50, got {overall}"

    def test_deterministic_scoring(self):
        """Same input must produce exact same output."""
        ctx = _make_context()
        engine = ScoringEngine()

        score1, _, _ = engine.run_all(ctx)
        score2, _, _ = engine.run_all(ctx)
        assert score1 == score2, "Scoring must be deterministic"

    def test_deprecated_schema_flagged(self):
        page = _make_page(
            schema_blocks=[{"@context": "https://schema.org", "@type": "HowTo", "name": "Test"}]
        )
        ctx = _make_context(pages={"https://example.com": page})

        engine = ScoringEngine()
        _, _, issues = engine.run_all(ctx)

        deprecated_check = next(
            (i for i in issues if i.check_id == "tech.structured.no_deprecated_schema"), None
        )
        assert deprecated_check is not None
        assert not deprecated_check.passed

    def test_noindex_homepage_flagged(self):
        page = _make_page(meta_robots="noindex", html='<meta name="robots" content="noindex">')
        ctx = _make_context(pages={"https://example.com": page})

        engine = ScoringEngine()
        _, _, issues = engine.run_all(ctx)

        noindex_check = next(
            (i for i in issues if i.check_id == "tech.crawl.no_accidental_noindex"), None
        )
        assert noindex_check is not None
        assert not noindex_check.passed

    def test_cwv_scoring(self):
        ctx = _make_context(cwv=CWVData(lcp_ms=1500, inp_ms=100, cls=0.05, source="field"))

        engine = ScoringEngine()
        _, categories, _ = engine.run_all(ctx)

        perf = next(c for c in categories if c.category == "performance")
        assert perf.score > 70, f"Good CWV should score >70, got {perf.score}"

    def test_cwv_poor_scoring(self):
        ctx = _make_context(cwv=CWVData(lcp_ms=5000, inp_ms=600, cls=0.3, source="field"))

        engine = ScoringEngine()
        _, categories, _ = engine.run_all(ctx)

        perf = next(c for c in categories if c.category == "performance")
        assert perf.score < 30, f"Poor CWV should score <30, got {perf.score}"

    def test_check_count(self):
        engine = ScoringEngine()
        assert len(engine._checks) >= 98, f"Expected 98+ checks, got {len(engine._checks)}"

    def test_gsc_checks_neutral_without_data(self):
        """GSC checks return 0.5 (neutral) when no GSC data provided."""
        ctx = _make_context()
        engine = ScoringEngine()
        _, _, issues = engine.run_all(ctx)
        gsc_checks = [i for i in issues if ".gsc." in i.check_id]
        assert len(gsc_checks) == 6, f"Expected 6 GSC checks, got {len(gsc_checks)}"
        for check in gsc_checks:
            assert check.score == 0.5, f"{check.check_id} should be 0.5 without GSC data, got {check.score}"

    def test_gsc_checks_with_good_data(self):
        """GSC checks score well with good search data."""
        sd = SearchData(
            total_pages=10, indexed_pages=10, coverage_errors=0,
            avg_position=8.5, avg_ctr=0.06, total_impressions=50000,
            total_clicks=3000, impressions_trend=1.15,
            page_impressions={"https://example.com": 5000},
            declining_pages=[], source="gsc",
        )
        ctx = _make_context()
        ctx["search_data"] = sd
        engine = ScoringEngine()
        _, _, issues = engine.run_all(ctx)
        gsc_checks = [i for i in issues if ".gsc." in i.check_id]
        for check in gsc_checks:
            assert check.score >= 0.7, f"{check.check_id} should score well with good data, got {check.score}"

    def test_gsc_checks_with_poor_data(self):
        """GSC checks score poorly with bad search data."""
        # Create 20 pages so coverage_ratio (indexed=2/total=20=10%) is low
        pages = {}
        for i in range(20):
            url = f"https://example.com/page-{i}" if i > 0 else "https://example.com"
            pages[url] = _make_page(url=url)
        sd = SearchData(
            total_pages=20, indexed_pages=2, coverage_errors=20,
            avg_position=55.0, avg_ctr=0.005, total_impressions=100,
            total_clicks=1, impressions_trend=0.4,
            page_impressions={"https://example.com": 10, "https://example.com/page-1": 5},
            declining_pages=[f"https://example.com/page-{i}" for i in range(8)],
            source="gsc",
        )
        ctx = _make_context(pages=pages)
        ctx["search_data"] = sd
        engine = ScoringEngine()
        _, _, issues = engine.run_all(ctx)
        gsc_checks = [i for i in issues if ".gsc." in i.check_id]
        for check in gsc_checks:
            assert check.score <= 0.5, f"{check.check_id} should score poorly with bad data, got {check.score}"


class TestAutoFixer:

    def test_generates_fixes(self):
        from engine.auto_fixer import AutoFixer

        page = _make_page(title=None, meta_desc=None, canonical=None, html="<html><body>test</body></html>")
        crawl = CrawlResult(start_url="https://example.com",
                            pages={"https://example.com": page})

        engine = ScoringEngine()
        ctx = _make_context(pages={"https://example.com": page}, robots_txt="")
        _, _, issues = engine.run_all(ctx)

        fixer = AutoFixer()
        fixes = fixer.generate_fixes(issues, crawl)
        assert len(fixes) > 0, "Should generate at least one fix"


class TestLinkGraph:

    def test_pagerank(self):
        from engine.link_graph import LinkGraph

        crawl = CrawlResult(start_url="https://example.com")
        crawl.pages = {
            "https://example.com": _make_page(url="https://example.com"),
            "https://example.com/a": _make_page(url="https://example.com/a"),
            "https://example.com/b": _make_page(url="https://example.com/b"),
        }
        crawl.link_graph = {
            "https://example.com": {"https://example.com/a", "https://example.com/b"},
            "https://example.com/a": {"https://example.com"},
            "https://example.com/b": set(),
        }

        lg = LinkGraph()
        result = lg.analyze(crawl)

        assert len(result.internal_pagerank) == 3
        assert result.dead_ends == ["https://example.com/b"]


if __name__ == "__main__":
    # Simple test runner without pytest
    import traceback
    test_classes = [TestScoringEngine, TestAutoFixer, TestLinkGraph]
    passed = failed = 0
    for cls in test_classes:
        instance = cls()
        for method_name in dir(instance):
            if method_name.startswith("test_"):
                try:
                    getattr(instance, method_name)()
                    print(f"  ✓ {cls.__name__}.{method_name}")
                    passed += 1
                except Exception as e:
                    print(f"  ✗ {cls.__name__}.{method_name}: {e}")
                    traceback.print_exc()
                    failed += 1
    print(f"\n{'='*40}\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
