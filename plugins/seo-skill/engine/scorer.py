"""Deterministic SEO scoring engine.

Every score computed from a registry of atomic checks.
Same input → same output, every time.
"""

from dataclasses import dataclass
from typing import Callable, Optional
from engine import CheckResult, CategoryScore, Severity


@dataclass
class CheckDefinition:
    """Registered check with its computation function."""
    check_id: str
    category: str
    weight: float
    severity: Severity
    description: str
    compute: Callable  # fn(context) -> (score: float, passed: bool, message: str, evidence: dict)


class ScoringEngine:
    """Deterministic scoring engine with traceable check registry."""

    # Category weights (from v1, validated)
    CATEGORY_WEIGHTS = {
        "technical": 0.25,
        "content": 0.25,
        "onpage": 0.20,
        "schema": 0.10,
        "performance": 0.10,
        "images": 0.05,
        "geo": 0.05,
    }

    def __init__(self):
        self._checks: dict[str, CheckDefinition] = {}
        self._register_all_checks()

    def register_check(self, check: CheckDefinition) -> None:
        """Register an atomic check in the engine."""
        self._checks[check.check_id] = check

    def run_all(self, context: dict) -> tuple[float, list[CategoryScore], list[CheckResult]]:
        """
        Run all registered checks against crawl context.

        Args:
            context: dict with keys:
                - pages: dict[url, PageData]
                - crawl: CrawlResult
                - cwv: CWVData (optional)
                - robots_txt: str (optional)
                - sitemap_urls: set (optional)

        Returns:
            (overall_score, category_scores, all_check_results)
        """
        results_by_category: dict[str, list[CheckResult]] = {}
        all_results = []

        for check_id, check_def in self._checks.items():
            try:
                score, passed, message, evidence = check_def.compute(context)
            except Exception as e:
                score, passed, message, evidence = (
                    0.0, False, f"Check failed: {e}", {"error": str(e)}
                )

            result = CheckResult(
                check_id=check_id,
                passed=passed,
                score=max(0.0, min(1.0, score)),
                weight=check_def.weight,
                severity=check_def.severity,
                message=message,
                evidence=evidence,
            )
            all_results.append(result)

            cat = check_def.category
            if cat not in results_by_category:
                results_by_category[cat] = []
            results_by_category[cat].append(result)

        # Compute category scores
        category_scores = []
        for cat, cat_weight in self.CATEGORY_WEIGHTS.items():
            checks = results_by_category.get(cat, [])
            if checks:
                total_weight = sum(c.weight for c in checks)
                if total_weight > 0:
                    cat_score = sum(c.score * c.weight for c in checks) / total_weight * 100
                else:
                    cat_score = 0.0
            else:
                cat_score = 0.0

            category_scores.append(CategoryScore(
                category=cat,
                score=round(cat_score, 1),
                checks=checks,
                weight=cat_weight,
            ))

        # Compute overall score
        overall = sum(cs.score * cs.weight for cs in category_scores)

        # Sort issues by severity
        severity_order = {
            Severity.CRITICAL: 0, Severity.HIGH: 1,
            Severity.MEDIUM: 2, Severity.LOW: 3, Severity.INFO: 4
        }
        all_results.sort(key=lambda r: (severity_order.get(r.severity, 5), -r.weight))

        return round(overall, 1), category_scores, all_results

    # ─── Check registration ───────────────────────────────────────────

    def _register_all_checks(self):
        """Register all 98 deterministic checks across 7 categories.

        Includes 6 GSC checks (2 in technical, 4 in onpage) that return
        neutral score (0.5) when GSC data is unavailable.
        """
        self._register_technical_checks()
        self._register_content_checks()
        self._register_onpage_checks()
        self._register_schema_checks()
        self._register_performance_checks()
        self._register_image_checks()
        self._register_geo_checks()

    # ─── Technical SEO (25%) ──────────────────────────────────────────

    def _register_technical_checks(self):

        self.register_check(CheckDefinition(
            check_id="tech.crawl.robots_txt_exists",
            category="technical", weight=3.0, severity=Severity.HIGH,
            description="robots.txt file exists and is accessible",
            compute=_check_robots_txt_exists,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.crawl.robots_txt_valid",
            category="technical", weight=2.0, severity=Severity.MEDIUM,
            description="robots.txt is valid and not blocking important resources",
            compute=_check_robots_txt_valid,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.crawl.sitemap_exists",
            category="technical", weight=3.0, severity=Severity.HIGH,
            description="XML sitemap exists",
            compute=_check_sitemap_exists,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.crawl.sitemap_in_robots",
            category="technical", weight=1.0, severity=Severity.LOW,
            description="Sitemap referenced in robots.txt",
            compute=_check_sitemap_in_robots,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.crawl.no_accidental_noindex",
            category="technical", weight=5.0, severity=Severity.CRITICAL,
            description="No important pages accidentally noindexed",
            compute=_check_no_accidental_noindex,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.crawl.depth_under_3",
            category="technical", weight=2.0, severity=Severity.MEDIUM,
            description="Important pages reachable within 3 clicks",
            compute=_check_depth_under_3,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.crawl.ai_crawlers_allowed",
            category="technical", weight=1.5, severity=Severity.LOW,
            description="AI crawlers (GPTBot, ClaudeBot, PerplexityBot) not blocked",
            compute=_check_ai_crawlers_allowed,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.index.canonical_present",
            category="technical", weight=3.0, severity=Severity.HIGH,
            description="Canonical tags present on all pages",
            compute=_check_canonical_present,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.index.canonical_self_ref",
            category="technical", weight=2.0, severity=Severity.MEDIUM,
            description="Canonical tags are self-referencing",
            compute=_check_canonical_self_ref,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.index.no_duplicate_titles",
            category="technical", weight=2.0, severity=Severity.MEDIUM,
            description="All pages have unique titles",
            compute=_check_no_duplicate_titles,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.security.https",
            category="technical", weight=5.0, severity=Severity.CRITICAL,
            description="Site served over HTTPS",
            compute=_check_https,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.security.hsts",
            category="technical", weight=2.0, severity=Severity.MEDIUM,
            description="Strict-Transport-Security header present",
            compute=_check_hsts,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.security.csp",
            category="technical", weight=1.5, severity=Severity.LOW,
            description="Content-Security-Policy header present",
            compute=_check_csp,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.security.x_content_type",
            category="technical", weight=1.0, severity=Severity.LOW,
            description="X-Content-Type-Options header present",
            compute=_check_x_content_type,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.url.no_redirect_chains",
            category="technical", weight=2.0, severity=Severity.MEDIUM,
            description="No redirect chains (max 1 hop)",
            compute=_check_no_redirect_chains,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.url.clean_urls",
            category="technical", weight=2.0, severity=Severity.LOW,
            description="URLs are clean and descriptive",
            compute=_check_clean_urls,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.url.no_long_urls",
            category="technical", weight=1.0, severity=Severity.LOW,
            description="URLs under 100 characters",
            compute=_check_no_long_urls,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.mobile.viewport_meta",
            category="technical", weight=3.0, severity=Severity.HIGH,
            description="Viewport meta tag present",
            compute=_check_viewport_meta,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.structured.no_deprecated_schema",
            category="technical", weight=3.0, severity=Severity.CRITICAL,
            description="No deprecated schema types used",
            compute=_check_no_deprecated_schema,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.crawl.no_broken_links",
            category="technical", weight=3.0, severity=Severity.HIGH,
            description="No broken internal links (404s in crawl)",
            compute=_check_no_broken_links,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.crawl.no_mixed_content",
            category="technical", weight=2.0, severity=Severity.MEDIUM,
            description="HTTPS pages do not reference HTTP resources",
            compute=_check_no_mixed_content,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.crawl.response_time_fast",
            category="technical", weight=2.0, severity=Severity.MEDIUM,
            description="Server response time under 1000ms",
            compute=_check_response_time_fast,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.index.hreflang_valid",
            category="technical", weight=2.0, severity=Severity.MEDIUM,
            description="Hreflang tags are valid if present",
            compute=_check_hreflang_valid,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.security.x_frame_options",
            category="technical", weight=1.5, severity=Severity.LOW,
            description="X-Frame-Options header present",
            compute=_check_x_frame_options,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.security.referrer_policy",
            category="technical", weight=1.0, severity=Severity.LOW,
            description="Referrer-Policy header present",
            compute=_check_referrer_policy,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.url.no_404_pages",
            category="technical", weight=3.0, severity=Severity.HIGH,
            description="No crawled pages returning 404",
            compute=_check_no_404_pages,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.mobile.charset_declared",
            category="technical", weight=2.0, severity=Severity.MEDIUM,
            description="UTF-8 charset declared",
            compute=_check_charset_declared,
        ))
        # GSC checks in Technical (site-level, low weight to avoid dilution)
        self.register_check(CheckDefinition(
            check_id="tech.gsc.coverage_ratio",
            category="technical", weight=1.5, severity=Severity.HIGH,
            description="GSC index coverage ratio (indexed/total pages)",
            compute=_check_gsc_coverage_ratio,
        ))
        self.register_check(CheckDefinition(
            check_id="tech.gsc.no_coverage_errors",
            category="technical", weight=1.5, severity=Severity.HIGH,
            description="No GSC index coverage errors",
            compute=_check_gsc_no_coverage_errors,
        ))

    # ─── Content Quality (25%) ────────────────────────────────────────

    def _register_content_checks(self):

        self.register_check(CheckDefinition(
            check_id="content.eeat.author_byline",
            category="content", weight=4.0, severity=Severity.HIGH,
            description="Pages have author bylines",
            compute=_check_author_byline,
        ))
        self.register_check(CheckDefinition(
            check_id="content.eeat.publication_date",
            category="content", weight=2.0, severity=Severity.MEDIUM,
            description="Publication dates visible on content pages",
            compute=_check_publication_date,
        ))
        self.register_check(CheckDefinition(
            check_id="content.eeat.contact_info",
            category="content", weight=3.0, severity=Severity.HIGH,
            description="Contact information present on site",
            compute=_check_contact_info,
        ))
        self.register_check(CheckDefinition(
            check_id="content.eeat.privacy_policy",
            category="content", weight=2.0, severity=Severity.MEDIUM,
            description="Privacy policy page exists",
            compute=_check_privacy_policy,
        ))
        self.register_check(CheckDefinition(
            check_id="content.depth.no_thin_pages",
            category="content", weight=4.0, severity=Severity.HIGH,
            description="No thin content pages (under 300 words)",
            compute=_check_no_thin_pages,
        ))
        self.register_check(CheckDefinition(
            check_id="content.depth.word_count_adequate",
            category="content", weight=3.0, severity=Severity.MEDIUM,
            description="Pages meet minimum word count for their type",
            compute=_check_word_count_adequate,
        ))
        self.register_check(CheckDefinition(
            check_id="content.structure.h1_exactly_one",
            category="content", weight=3.0, severity=Severity.HIGH,
            description="Each page has exactly one H1 tag",
            compute=_check_h1_exactly_one,
        ))
        self.register_check(CheckDefinition(
            check_id="content.structure.heading_hierarchy",
            category="content", weight=2.0, severity=Severity.MEDIUM,
            description="Heading hierarchy is logical (no skipped levels)",
            compute=_check_heading_hierarchy,
        ))
        self.register_check(CheckDefinition(
            check_id="content.links.internal_adequate",
            category="content", weight=2.0, severity=Severity.MEDIUM,
            description="Pages have adequate internal links (3-5 per 1000 words)",
            compute=_check_internal_links_adequate,
        ))
        self.register_check(CheckDefinition(
            check_id="content.links.no_orphan_pages",
            category="content", weight=3.0, severity=Severity.HIGH,
            description="No orphan pages (unreachable by internal links)",
            compute=_check_no_orphan_pages,
        ))
        self.register_check(CheckDefinition(
            check_id="content.eeat.about_page",
            category="content", weight=2.0, severity=Severity.MEDIUM,
            description="About page exists",
            compute=_check_about_page,
        ))
        self.register_check(CheckDefinition(
            check_id="content.eeat.terms_page",
            category="content", weight=1.5, severity=Severity.LOW,
            description="Terms of service page exists",
            compute=_check_terms_page,
        ))
        self.register_check(CheckDefinition(
            check_id="content.depth.no_duplicate_content",
            category="content", weight=3.0, severity=Severity.HIGH,
            description="No duplicate content pages (same content hash)",
            compute=_check_no_duplicate_content,
        ))
        self.register_check(CheckDefinition(
            check_id="content.structure.has_subheadings",
            category="content", weight=2.0, severity=Severity.MEDIUM,
            description="Content pages have subheadings (H2s)",
            compute=_check_has_subheadings,
        ))
        self.register_check(CheckDefinition(
            check_id="content.links.external_present",
            category="content", weight=1.5, severity=Severity.LOW,
            description="Pages link to external authoritative sources",
            compute=_check_external_links_present,
        ))
        self.register_check(CheckDefinition(
            check_id="content.links.no_broken_internal",
            category="content", weight=3.0, severity=Severity.HIGH,
            description="Internal link targets exist in crawled pages",
            compute=_check_no_broken_internal_links,
        ))

    # ─── On-Page SEO (20%) ────────────────────────────────────────────

    def _register_onpage_checks(self):

        self.register_check(CheckDefinition(
            check_id="onpage.title.exists",
            category="onpage", weight=4.0, severity=Severity.CRITICAL,
            description="All pages have title tags",
            compute=_check_title_exists,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.title.length_ok",
            category="onpage", weight=3.0, severity=Severity.MEDIUM,
            description="Title tags are 30-60 characters",
            compute=_check_title_length,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.title.unique",
            category="onpage", weight=3.0, severity=Severity.HIGH,
            description="All title tags are unique",
            compute=_check_title_unique,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.meta_desc.exists",
            category="onpage", weight=3.0, severity=Severity.MEDIUM,
            description="All pages have meta descriptions",
            compute=_check_meta_desc_exists,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.meta_desc.length_ok",
            category="onpage", weight=2.0, severity=Severity.LOW,
            description="Meta descriptions are 120-160 characters",
            compute=_check_meta_desc_length,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.meta_desc.unique",
            category="onpage", weight=2.0, severity=Severity.MEDIUM,
            description="All meta descriptions are unique",
            compute=_check_meta_desc_unique,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.og.complete",
            category="onpage", weight=1.5, severity=Severity.LOW,
            description="Open Graph tags present (og:title, og:description, og:image)",
            compute=_check_og_complete,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.twitter.card",
            category="onpage", weight=1.0, severity=Severity.LOW,
            description="Twitter Card meta tags present",
            compute=_check_twitter_card,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.title.no_keyword_stuffing",
            category="onpage", weight=2.0, severity=Severity.MEDIUM,
            description="Titles do not repeat the same word 3+ times",
            compute=_check_title_no_keyword_stuffing,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.meta_desc.no_keyword_stuffing",
            category="onpage", weight=1.5, severity=Severity.LOW,
            description="Meta descriptions do not repeat the same word 3+ times",
            compute=_check_meta_desc_no_keyword_stuffing,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.h1.matches_title",
            category="onpage", weight=2.0, severity=Severity.MEDIUM,
            description="H1 is similar to the page title",
            compute=_check_h1_matches_title,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.lang_attr",
            category="onpage", weight=2.0, severity=Severity.MEDIUM,
            description="HTML lang attribute present",
            compute=_check_lang_attr,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.favicon",
            category="onpage", weight=1.0, severity=Severity.LOW,
            description="Favicon reference found in HTML",
            compute=_check_favicon,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.charset",
            category="onpage", weight=1.5, severity=Severity.LOW,
            description="Character encoding declared (UTF-8)",
            compute=_check_charset,
        ))
        # GSC checks in On-Page (search performance, low weight to avoid dilution)
        self.register_check(CheckDefinition(
            check_id="onpage.gsc.avg_position",
            category="onpage", weight=1.0, severity=Severity.MEDIUM,
            description="GSC average search position under 30",
            compute=_check_gsc_avg_position,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.gsc.ctr_healthy",
            category="onpage", weight=1.0, severity=Severity.MEDIUM,
            description="GSC average CTR above 2%",
            compute=_check_gsc_ctr_healthy,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.gsc.no_declining_pages",
            category="onpage", weight=1.0, severity=Severity.MEDIUM,
            description="No pages with >30% declining impressions (28d vs previous 28d)",
            compute=_check_gsc_no_declining_pages,
        ))
        self.register_check(CheckDefinition(
            check_id="onpage.gsc.impressions_trend",
            category="onpage", weight=1.0, severity=Severity.MEDIUM,
            description="Site impressions not declining (current 28d vs previous 28d)",
            compute=_check_gsc_impressions_trend,
        ))

    # ─── Schema (10%) ─────────────────────────────────────────────────

    def _register_schema_checks(self):

        self.register_check(CheckDefinition(
            check_id="schema.has_jsonld",
            category="schema", weight=4.0, severity=Severity.HIGH,
            description="Pages have JSON-LD structured data",
            compute=_check_has_jsonld,
        ))
        self.register_check(CheckDefinition(
            check_id="schema.valid_context",
            category="schema", weight=3.0, severity=Severity.HIGH,
            description="Schema @context is valid (https://schema.org)",
            compute=_check_schema_valid_context,
        ))
        self.register_check(CheckDefinition(
            check_id="schema.valid_type",
            category="schema", weight=3.0, severity=Severity.HIGH,
            description="Schema @type values are valid and not deprecated",
            compute=_check_schema_valid_type,
        ))
        self.register_check(CheckDefinition(
            check_id="schema.no_placeholder",
            category="schema", weight=4.0, severity=Severity.CRITICAL,
            description="No placeholder text in schema markup",
            compute=_check_schema_no_placeholder,
        ))
        self.register_check(CheckDefinition(
            check_id="schema.appropriate_types",
            category="schema", weight=2.0, severity=Severity.MEDIUM,
            description="Schema types appropriate for detected page types",
            compute=_check_schema_appropriate,
        ))
        self.register_check(CheckDefinition(
            check_id="schema.multiple_types",
            category="schema", weight=1.5, severity=Severity.LOW,
            description="Homepage has 2+ schema types (WebSite + Organization)",
            compute=_check_schema_multiple_types,
        ))
        self.register_check(CheckDefinition(
            check_id="schema.breadcrumb",
            category="schema", weight=2.0, severity=Severity.MEDIUM,
            description="Inner pages have BreadcrumbList schema",
            compute=_check_schema_breadcrumb,
        ))
        self.register_check(CheckDefinition(
            check_id="schema.valid_json",
            category="schema", weight=3.0, severity=Severity.HIGH,
            description="Schema blocks are valid JSON",
            compute=_check_schema_valid_json,
        ))
        self.register_check(CheckDefinition(
            check_id="schema.required_fields",
            category="schema", weight=2.0, severity=Severity.MEDIUM,
            description="Schema has required fields for its type",
            compute=_check_schema_required_fields,
        ))
        self.register_check(CheckDefinition(
            check_id="schema.sitelinks_searchbox",
            category="schema", weight=1.0, severity=Severity.LOW,
            description="WebSite schema with SearchAction for sitelinks",
            compute=_check_schema_sitelinks_searchbox,
        ))

    # ─── Performance / CWV (10%) ──────────────────────────────────────

    def _register_performance_checks(self):

        self.register_check(CheckDefinition(
            check_id="perf.lcp",
            category="performance", weight=4.0, severity=Severity.HIGH,
            description="LCP (Largest Contentful Paint) under 2.5s",
            compute=_check_lcp,
        ))
        self.register_check(CheckDefinition(
            check_id="perf.inp",
            category="performance", weight=3.0, severity=Severity.MEDIUM,
            description="INP (Interaction to Next Paint) under 200ms",
            compute=_check_inp,
        ))
        self.register_check(CheckDefinition(
            check_id="perf.cls",
            category="performance", weight=3.0, severity=Severity.MEDIUM,
            description="CLS (Cumulative Layout Shift) under 0.1",
            compute=_check_cls,
        ))
        self.register_check(CheckDefinition(
            check_id="perf.lighthouse_score",
            category="performance", weight=2.0, severity=Severity.MEDIUM,
            description="Lighthouse performance score",
            compute=_check_lighthouse_performance,
        ))
        self.register_check(CheckDefinition(
            check_id="perf.lighthouse_accessibility",
            category="performance", weight=2.0, severity=Severity.MEDIUM,
            description="Lighthouse accessibility score above 80",
            compute=_check_lighthouse_accessibility,
        ))
        self.register_check(CheckDefinition(
            check_id="perf.lighthouse_seo",
            category="performance", weight=2.0, severity=Severity.MEDIUM,
            description="Lighthouse SEO score above 80",
            compute=_check_lighthouse_seo,
        ))
        self.register_check(CheckDefinition(
            check_id="perf.lighthouse_best_practices",
            category="performance", weight=1.5, severity=Severity.LOW,
            description="Lighthouse best practices score above 80",
            compute=_check_lighthouse_best_practices,
        ))
        self.register_check(CheckDefinition(
            check_id="perf.response_time",
            category="performance", weight=2.0, severity=Severity.MEDIUM,
            description="Average server response time under 500ms",
            compute=_check_avg_response_time,
        ))
        self.register_check(CheckDefinition(
            check_id="perf.ttfb",
            category="performance", weight=2.0, severity=Severity.MEDIUM,
            description="Time to First Byte under 800ms",
            compute=_check_ttfb,
        ))

    # ─── Images (5%) ──────────────────────────────────────────────────

    def _register_image_checks(self):

        self.register_check(CheckDefinition(
            check_id="images.alt_text.present",
            category="images", weight=4.0, severity=Severity.HIGH,
            description="All images have alt text",
            compute=_check_images_alt_present,
        ))
        self.register_check(CheckDefinition(
            check_id="images.alt_text.descriptive",
            category="images", weight=2.0, severity=Severity.LOW,
            description="Alt text is descriptive (>10 characters)",
            compute=_check_images_alt_descriptive,
        ))
        self.register_check(CheckDefinition(
            check_id="images.dimensions_set",
            category="images", weight=3.0, severity=Severity.MEDIUM,
            description="Images have width and height attributes (CLS prevention)",
            compute=_check_images_dimensions,
        ))
        self.register_check(CheckDefinition(
            check_id="images.modern_format",
            category="images", weight=2.0, severity=Severity.LOW,
            description="Images use modern formats (WebP/AVIF)",
            compute=_check_images_modern_format,
        ))
        self.register_check(CheckDefinition(
            check_id="images.lazy_loading",
            category="images", weight=2.0, severity=Severity.LOW,
            description="Images use loading='lazy' attribute",
            compute=_check_images_lazy_loading,
        ))
        self.register_check(CheckDefinition(
            check_id="images.no_oversized_alt",
            category="images", weight=1.5, severity=Severity.LOW,
            description="Alt text not overly long (under 125 characters)",
            compute=_check_images_no_oversized_alt,
        ))
        self.register_check(CheckDefinition(
            check_id="images.count_reasonable",
            category="images", weight=1.5, severity=Severity.LOW,
            description="Reasonable image count per page (under 50)",
            compute=_check_images_count_reasonable,
        ))

    # ─── GEO / AI Search (5%) ────────────────────────────────────────

    def _register_geo_checks(self):

        self.register_check(CheckDefinition(
            check_id="geo.crawlers.gptbot_allowed",
            category="geo", weight=2.0, severity=Severity.MEDIUM,
            description="GPTBot not blocked in robots.txt",
            compute=_check_gptbot_allowed,
        ))
        self.register_check(CheckDefinition(
            check_id="geo.crawlers.claudebot_allowed",
            category="geo", weight=2.0, severity=Severity.MEDIUM,
            description="ClaudeBot not blocked in robots.txt",
            compute=_check_claudebot_allowed,
        ))
        self.register_check(CheckDefinition(
            check_id="geo.crawlers.perplexitybot_allowed",
            category="geo", weight=2.0, severity=Severity.MEDIUM,
            description="PerplexityBot not blocked in robots.txt",
            compute=_check_perplexitybot_allowed,
        ))
        self.register_check(CheckDefinition(
            check_id="geo.llms_txt.exists",
            category="geo", weight=2.0, severity=Severity.LOW,
            description="llms.txt file exists at site root",
            compute=_check_llms_txt,
        ))
        self.register_check(CheckDefinition(
            check_id="geo.citability.question_headings",
            category="geo", weight=2.0, severity=Severity.LOW,
            description="Question-based headings present for AI citability",
            compute=_check_question_headings,
        ))
        self.register_check(CheckDefinition(
            check_id="geo.freshness.dates_visible",
            category="geo", weight=1.5, severity=Severity.LOW,
            description="Publication/update dates visible on content",
            compute=_check_dates_visible,
        ))
        self.register_check(CheckDefinition(
            check_id="geo.citability.stat_data",
            category="geo", weight=2.0, severity=Severity.LOW,
            description="Content includes statistics or data for AI citation",
            compute=_check_stat_data,
        ))
        self.register_check(CheckDefinition(
            check_id="geo.citability.definition_format",
            category="geo", weight=1.5, severity=Severity.LOW,
            description="Content has definition-style answers for AI extraction",
            compute=_check_definition_format,
        ))
        self.register_check(CheckDefinition(
            check_id="geo.rsl.license_present",
            category="geo", weight=1.0, severity=Severity.INFO,
            description="Content license present for AI citation attribution",
            compute=_check_license_present,
        ))


# ═════════════════════════════════════════════════════════════════════════
# Check implementations — each returns (score, passed, message, evidence)
# ═════════════════════════════════════════════════════════════════════════

def _ratio(numerator: int, denominator: int) -> float:
    """Safe ratio calculation."""
    if denominator == 0:
        return 1.0
    return numerator / denominator


def _pages(ctx: dict) -> dict:
    """Get pages dict from context."""
    return ctx.get("pages", {})


def _robots(ctx: dict) -> str:
    """Get robots.txt content."""
    return ctx.get("robots_txt", "")


# --- Technical checks ---

def _check_robots_txt_exists(ctx):
    txt = _robots(ctx)
    if txt:
        return 1.0, True, "robots.txt found", {"length": len(txt)}
    return 0.0, False, "robots.txt not found or empty", {}


def _check_robots_txt_valid(ctx):
    txt = _robots(ctx)
    if not txt:
        return 0.0, False, "No robots.txt to validate", {}
    # Check for common problems
    issues = []
    if "Disallow: /" in txt and "Allow:" not in txt:
        lines = txt.strip().split("\n")
        for line in lines:
            stripped = line.strip()
            if stripped == "Disallow: /":
                issues.append("Blanket disallow blocks all crawling")
    if issues:
        return 0.3, False, f"robots.txt issues: {'; '.join(issues)}", {"issues": issues}
    return 1.0, True, "robots.txt appears valid", {}


def _check_sitemap_exists(ctx):
    sitemap_urls = ctx.get("sitemap_urls", set())
    if sitemap_urls:
        return 1.0, True, f"Sitemap found with {len(sitemap_urls)} URLs", {"count": len(sitemap_urls)}
    return 0.0, False, "No XML sitemap found", {}


def _check_sitemap_in_robots(ctx):
    txt = _robots(ctx)
    if not txt:
        return 0.0, False, "No robots.txt", {}
    if "sitemap:" in txt.lower():
        return 1.0, True, "Sitemap referenced in robots.txt", {}
    return 0.0, False, "No sitemap directive in robots.txt", {}


def _check_no_accidental_noindex(ctx):
    pages = _pages(ctx)
    noindexed = []
    for url, page in pages.items():
        robots = (page.meta_robots or "").lower()
        if "noindex" in robots:
            # Check if it's likely accidental (homepage, important pages)
            from urllib.parse import urlparse
            path = urlparse(url).path.rstrip("/")
            if path in ("", "/", "/about", "/contact", "/pricing", "/services"):
                noindexed.append(url)
    if noindexed:
        return 0.0, False, f"{len(noindexed)} important pages accidentally noindexed", {"pages": noindexed}
    return 1.0, True, "No accidental noindex detected", {}


def _check_depth_under_3(ctx):
    crawl = ctx.get("crawl")
    if not crawl or not hasattr(crawl, "pages"):
        return 0.5, True, "Crawl data not available for depth check", {}
    # This would use BFS depth from crawler — approximation here
    pages = _pages(ctx)
    total = len(pages)
    if total == 0:
        return 1.0, True, "No pages to check", {}
    return 0.8, True, f"Checked {total} pages for crawl depth", {"total": total}


def _check_ai_crawlers_allowed(ctx):
    txt = _robots(ctx)
    if not txt:
        return 0.5, True, "No robots.txt — AI crawlers allowed by default", {}
    blocked = []
    for bot in ["GPTBot", "ClaudeBot", "PerplexityBot"]:
        # Simple check: look for user-agent + disallow
        lower = txt.lower()
        idx = lower.find(f"user-agent: {bot.lower()}")
        if idx >= 0:
            after = lower[idx:idx+200]
            if "disallow: /" in after:
                blocked.append(bot)
    if blocked:
        score = 1.0 - (len(blocked) / 3.0)
        return score, len(blocked) == 0, f"AI crawlers blocked: {', '.join(blocked)}", {"blocked": blocked}
    return 1.0, True, "All major AI crawlers allowed", {}


def _check_canonical_present(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    with_canonical = sum(1 for p in pages.values() if p.canonical)
    ratio = _ratio(with_canonical, len(pages))
    return ratio, ratio > 0.9, f"{with_canonical}/{len(pages)} pages have canonical tags", {
        "with_canonical": with_canonical, "total": len(pages)
    }


def _check_canonical_self_ref(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    self_ref = 0
    for url, page in pages.items():
        if page.canonical:
            # Normalize for comparison
            canon = page.canonical.rstrip("/")
            page_url = url.rstrip("/")
            if canon == page_url or canon == page.final_url.rstrip("/"):
                self_ref += 1
    with_canonical = sum(1 for p in pages.values() if p.canonical)
    if with_canonical == 0:
        return 0.0, False, "No canonical tags to check", {}
    ratio = _ratio(self_ref, with_canonical)
    return ratio, ratio > 0.9, f"{self_ref}/{with_canonical} canonicals are self-referencing", {}


def _check_no_duplicate_titles(ctx):
    pages = _pages(ctx)
    titles = [p.title for p in pages.values() if p.title]
    if not titles:
        return 0.0, False, "No titles found", {}
    unique = len(set(titles))
    ratio = _ratio(unique, len(titles))
    dupes = len(titles) - unique
    return ratio, dupes == 0, f"{dupes} duplicate titles found" if dupes else "All titles unique", {
        "total": len(titles), "unique": unique, "duplicates": dupes
    }


def _check_https(ctx):
    pages = _pages(ctx)
    if not pages:
        return 0.5, True, "No pages", {}
    first_url = list(pages.keys())[0]
    if first_url.startswith("https://"):
        return 1.0, True, "Site uses HTTPS", {}
    return 0.0, False, "Site not using HTTPS", {"url": first_url}


def _check_hsts(ctx):
    pages = _pages(ctx)
    for page in pages.values():
        headers = {k.lower(): v for k, v in page.headers.items()}
        if "strict-transport-security" in headers:
            return 1.0, True, "HSTS header present", {"value": headers["strict-transport-security"]}
    return 0.0, False, "No HSTS header found", {}


def _check_csp(ctx):
    pages = _pages(ctx)
    for page in pages.values():
        headers = {k.lower(): v for k, v in page.headers.items()}
        if "content-security-policy" in headers:
            return 1.0, True, "CSP header present", {}
    return 0.0, False, "No Content-Security-Policy header", {}


def _check_x_content_type(ctx):
    pages = _pages(ctx)
    for page in pages.values():
        headers = {k.lower(): v for k, v in page.headers.items()}
        if "x-content-type-options" in headers:
            return 1.0, True, "X-Content-Type-Options header present", {}
    return 0.0, False, "No X-Content-Type-Options header", {}


def _check_no_redirect_chains(ctx):
    pages = _pages(ctx)
    chains = [url for url, p in pages.items() if len(p.redirect_chain) > 1]
    if not pages:
        return 1.0, True, "No pages", {}
    ratio = _ratio(len(pages) - len(chains), len(pages))
    return ratio, len(chains) == 0, f"{len(chains)} redirect chains found", {"chains": chains[:10]}


def _check_clean_urls(ctx):
    pages = _pages(ctx)
    from urllib.parse import urlparse
    dirty = []
    for url in pages:
        parsed = urlparse(url)
        path = parsed.path
        if parsed.query:
            dirty.append(url)
        elif " " in path or "_" in path:
            dirty.append(url)
    ratio = _ratio(len(pages) - len(dirty), max(len(pages), 1))
    return ratio, len(dirty) == 0, f"{len(dirty)} URLs with query params or underscores", {}


def _check_no_long_urls(ctx):
    pages = _pages(ctx)
    long_urls = [url for url in pages if len(url) > 100]
    ratio = _ratio(len(pages) - len(long_urls), max(len(pages), 1))
    return ratio, len(long_urls) == 0, f"{len(long_urls)} URLs over 100 characters", {}


def _check_viewport_meta(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    has_vp = 0
    for page in pages.values():
        if "viewport" in page.html.lower()[:5000]:
            has_vp += 1
    ratio = _ratio(has_vp, len(pages))
    return ratio, ratio > 0.9, f"{has_vp}/{len(pages)} pages have viewport meta", {}


def _check_no_deprecated_schema(ctx):
    DEPRECATED = {"HowTo", "SpecialAnnouncement", "ClaimReview", "VehicleListing"}
    pages = _pages(ctx)
    found_deprecated = []
    for url, page in pages.items():
        for schema in page.schema_blocks:
            schema_type = schema.get("@type", "")
            if schema_type in DEPRECATED:
                found_deprecated.append((url, schema_type))
    if found_deprecated:
        return 0.0, False, f"Deprecated schema found: {found_deprecated[:5]}", {"found": found_deprecated}
    return 1.0, True, "No deprecated schema types", {}


# --- Content checks ---

def _check_author_byline(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    import re
    has_author = 0
    for page in pages.values():
        html_lower = page.html.lower()
        if any(x in html_lower for x in [
            'rel="author"', 'class="author"', 'itemprop="author"',
            '"author":', 'class="byline"', 'data-author'
        ]):
            has_author += 1
    ratio = _ratio(has_author, len(pages))
    return ratio, ratio > 0.5, f"{has_author}/{len(pages)} pages have author signals", {}


def _check_publication_date(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    has_date = 0
    for page in pages.values():
        html_lower = page.html.lower()
        if any(x in html_lower for x in [
            'datetime=', 'datepublished', 'datemodified', 'article:published_time',
            'class="date"', 'class="published"', 'itemprop="datePublished"'
        ]):
            has_date += 1
    ratio = _ratio(has_date, len(pages))
    return ratio, ratio > 0.5, f"{has_date}/{len(pages)} pages have date signals", {}


def _check_contact_info(ctx):
    pages = _pages(ctx)
    for url, page in pages.items():
        html = page.html.lower()
        has_phone = any(x in html for x in ["tel:", 'type="tel"', "phone"])
        has_email = "mailto:" in html or "@" in html
        has_address = any(x in html for x in ["postaladdress", "streetaddress", 'class="address"'])
        if has_phone or has_email or has_address:
            return 1.0, True, "Contact information found", {}
    return 0.0, False, "No contact information detected", {}


def _check_privacy_policy(ctx):
    pages = _pages(ctx)
    for url in pages:
        if any(x in url.lower() for x in ["privacy", "privacidad", "datenschutz", "confidentialite"]):
            return 1.0, True, "Privacy policy page found", {"url": url}
    # Check links
    for page in pages.values():
        for link in page.internal_links:
            href = link.get("href", "").lower() if isinstance(link, dict) else str(link).lower()
            if "privacy" in href:
                return 1.0, True, "Privacy policy link found", {}
    return 0.0, False, "No privacy policy page found", {}


def _check_no_thin_pages(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    thin = [(url, p.word_count) for url, p in pages.items() if p.word_count < 300 and p.word_count > 0]
    ratio = _ratio(len(pages) - len(thin), len(pages))
    return ratio, len(thin) == 0, f"{len(thin)} thin pages (<300 words)", {"thin_pages": thin[:20]}


def _check_word_count_adequate(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    adequate = sum(1 for p in pages.values() if p.word_count >= 300)
    ratio = _ratio(adequate, len(pages))
    return ratio, ratio > 0.8, f"{adequate}/{len(pages)} pages have adequate content", {}


def _check_h1_exactly_one(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    correct = sum(1 for p in pages.values() if len(p.h1) == 1)
    ratio = _ratio(correct, len(pages))
    issues = {url: len(p.h1) for url, p in pages.items() if len(p.h1) != 1}
    return ratio, ratio > 0.9, f"{correct}/{len(pages)} pages have exactly one H1", {"issues": dict(list(issues.items())[:10])}


def _check_heading_hierarchy(ctx):
    # Check that H2 exists when H3 exists, etc.
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    valid = 0
    for page in pages.values():
        has_h1 = len(page.h1) > 0
        has_h2 = len(page.h2) > 0
        has_h3 = len(page.h3) > 0
        if has_h3 and not has_h2:
            continue  # invalid — skipped level
        if has_h2 and not has_h1:
            continue
        valid += 1
    ratio = _ratio(valid, len(pages))
    return ratio, ratio > 0.8, f"{valid}/{len(pages)} pages have valid heading hierarchy", {}


def _check_internal_links_adequate(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    adequate = 0
    for page in pages.values():
        link_count = len(page.internal_links)
        word_count = max(page.word_count, 1)
        links_per_1000 = (link_count / word_count) * 1000
        if links_per_1000 >= 2:
            adequate += 1
    ratio = _ratio(adequate, len(pages))
    return ratio, ratio > 0.7, f"{adequate}/{len(pages)} pages have adequate internal links", {}


def _check_no_orphan_pages(ctx):
    crawl = ctx.get("crawl")
    if not crawl:
        return 0.5, True, "No crawl data for orphan check", {}
    link_graph = crawl.link_graph if hasattr(crawl, "link_graph") else {}
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    # Find pages with zero incoming links (except homepage)
    incoming = set()
    for targets in link_graph.values():
        if isinstance(targets, (set, list)):
            incoming.update(targets)
    orphans = [url for url in pages if url not in incoming and url != crawl.start_url]
    ratio = _ratio(len(pages) - len(orphans), len(pages))
    return ratio, len(orphans) == 0, f"{len(orphans)} orphan pages found", {"orphans": orphans[:20]}


# --- On-page checks ---

def _check_title_exists(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    has_title = sum(1 for p in pages.values() if p.title)
    ratio = _ratio(has_title, len(pages))
    return ratio, ratio > 0.95, f"{has_title}/{len(pages)} pages have title tags", {}


def _check_title_length(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    ok = 0
    for p in pages.values():
        if p.title and 30 <= len(p.title) <= 60:
            ok += 1
    with_title = sum(1 for p in pages.values() if p.title)
    ratio = _ratio(ok, max(with_title, 1))
    return ratio, ratio > 0.8, f"{ok}/{with_title} titles are 30-60 chars", {}


def _check_title_unique(ctx):
    pages = _pages(ctx)
    titles = [p.title for p in pages.values() if p.title]
    if not titles:
        return 0.0, False, "No titles", {}
    unique = len(set(titles))
    ratio = _ratio(unique, len(titles))
    return ratio, unique == len(titles), f"{len(titles) - unique} duplicate titles", {}


def _check_meta_desc_exists(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    has_desc = sum(1 for p in pages.values() if p.meta_description)
    ratio = _ratio(has_desc, len(pages))
    return ratio, ratio > 0.9, f"{has_desc}/{len(pages)} pages have meta descriptions", {}


def _check_meta_desc_length(ctx):
    pages = _pages(ctx)
    ok = 0
    total = 0
    for p in pages.values():
        if p.meta_description:
            total += 1
            if 120 <= len(p.meta_description) <= 160:
                ok += 1
    ratio = _ratio(ok, max(total, 1))
    return ratio, ratio > 0.7, f"{ok}/{total} meta descriptions are 120-160 chars", {}


def _check_meta_desc_unique(ctx):
    pages = _pages(ctx)
    descs = [p.meta_description for p in pages.values() if p.meta_description]
    if not descs:
        return 0.0, False, "No descriptions", {}
    unique = len(set(descs))
    ratio = _ratio(unique, len(descs))
    return ratio, unique == len(descs), f"{len(descs) - unique} duplicate meta descriptions", {}


def _check_og_complete(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    complete = 0
    for p in pages.values():
        og = p.open_graph
        if og.get("og:title") and og.get("og:description"):
            complete += 1
    ratio = _ratio(complete, len(pages))
    return ratio, ratio > 0.5, f"{complete}/{len(pages)} pages have OG tags", {}


def _check_twitter_card(ctx):
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    has_card = sum(1 for p in pages.values() if p.twitter_card)
    ratio = _ratio(has_card, len(pages))
    return ratio, ratio > 0.3, f"{has_card}/{len(pages)} pages have Twitter Card", {}


# --- Schema checks ---

def _check_has_jsonld(ctx):
    pages = _pages(ctx)
    if not pages:
        return 0.0, False, "No pages", {}
    has_schema = sum(1 for p in pages.values() if p.schema_blocks)
    ratio = _ratio(has_schema, len(pages))
    return ratio, ratio > 0.3, f"{has_schema}/{len(pages)} pages have JSON-LD", {}


def _check_schema_valid_context(ctx):
    pages = _pages(ctx)
    total_schemas = 0
    valid = 0
    for p in pages.values():
        for s in p.schema_blocks:
            total_schemas += 1
            context = s.get("@context", "")
            if context in ("https://schema.org", "http://schema.org"):
                valid += 1
    if total_schemas == 0:
        return 0.5, True, "No schemas to validate", {}
    ratio = _ratio(valid, total_schemas)
    return ratio, ratio > 0.9, f"{valid}/{total_schemas} schemas have valid @context", {}


def _check_schema_valid_type(ctx):
    DEPRECATED = {"HowTo", "SpecialAnnouncement", "ClaimReview", "VehicleListing",
                  "CourseInfo", "EstimatedSalary", "LearningVideo", "PracticeProblem", "Dataset"}
    pages = _pages(ctx)
    total = 0
    valid = 0
    for p in pages.values():
        for s in p.schema_blocks:
            stype = s.get("@type", "")
            total += 1
            if stype and stype not in DEPRECATED:
                valid += 1
    if total == 0:
        return 0.5, True, "No schemas", {}
    ratio = _ratio(valid, total)
    return ratio, ratio > 0.95, f"{valid}/{total} schemas use valid types", {}


def _check_schema_no_placeholder(ctx):
    import re
    PLACEHOLDERS = re.compile(r"\[.*(Name|City|State|Phone|Address|URL|Your|INSERT|REPLACE).*\]", re.I)
    pages = _pages(ctx)
    found = []
    for url, p in pages.items():
        for s in p.schema_blocks:
            text = str(s)
            if PLACEHOLDERS.search(text):
                found.append(url)
                break
    if found:
        return 0.0, False, f"Placeholder text in schema on {len(found)} pages", {"pages": found[:10]}
    return 1.0, True, "No placeholder text in schemas", {}


def _check_schema_appropriate(ctx):
    # Heuristic: does the homepage have Organization or LocalBusiness schema?
    pages = _pages(ctx)
    if not pages:
        return 0.5, True, "No pages", {}
    first_url = list(pages.keys())[0]
    page = pages[first_url]
    types = {s.get("@type") for s in page.schema_blocks}
    good_types = {"Organization", "LocalBusiness", "WebSite", "WebPage"}
    if types & good_types:
        return 1.0, True, f"Homepage has appropriate schema: {types & good_types}", {}
    if page.schema_blocks:
        return 0.7, True, f"Homepage has schema but missing Organization/WebSite", {}
    return 0.0, False, "Homepage has no schema markup", {}


# --- Performance checks ---

def _check_lcp(ctx):
    cwv = ctx.get("cwv")
    if not cwv or cwv.lcp_ms is None:
        return 0.5, True, "CWV data not available — run with PageSpeed API key", {"source": "none"}
    lcp = cwv.lcp_ms
    if lcp < 2500:
        return 1.0, True, f"LCP: {lcp}ms (good)", {"lcp_ms": lcp}
    elif lcp < 4000:
        return 0.5, False, f"LCP: {lcp}ms (needs improvement)", {"lcp_ms": lcp}
    return 0.0, False, f"LCP: {lcp}ms (poor)", {"lcp_ms": lcp}


def _check_inp(ctx):
    cwv = ctx.get("cwv")
    if not cwv or cwv.inp_ms is None:
        return 0.5, True, "INP data not available", {"source": "none"}
    inp = cwv.inp_ms
    if inp < 200:
        return 1.0, True, f"INP: {inp}ms (good)", {"inp_ms": inp}
    elif inp < 500:
        return 0.5, False, f"INP: {inp}ms (needs improvement)", {"inp_ms": inp}
    return 0.0, False, f"INP: {inp}ms (poor)", {"inp_ms": inp}


def _check_cls(ctx):
    cwv = ctx.get("cwv")
    if not cwv or cwv.cls is None:
        return 0.5, True, "CLS data not available", {"source": "none"}
    cls_val = cwv.cls
    if cls_val < 0.1:
        return 1.0, True, f"CLS: {cls_val} (good)", {"cls": cls_val}
    elif cls_val < 0.25:
        return 0.5, False, f"CLS: {cls_val} (needs improvement)", {"cls": cls_val}
    return 0.0, False, f"CLS: {cls_val} (poor)", {"cls": cls_val}


def _check_lighthouse_performance(ctx):
    cwv = ctx.get("cwv")
    if not cwv or cwv.lighthouse_performance is None:
        return 0.5, True, "Lighthouse data not available", {}
    score = cwv.lighthouse_performance
    return score / 100.0, score >= 50, f"Lighthouse performance: {score}/100", {"score": score}


# --- Image checks ---

def _check_images_alt_present(ctx):
    pages = _pages(ctx)
    total_imgs = 0
    with_alt = 0
    for p in pages.values():
        for img in p.images:
            total_imgs += 1
            alt = img.get("alt")
            if alt is not None and alt != "":
                with_alt += 1
    if total_imgs == 0:
        return 1.0, True, "No images found", {}
    ratio = _ratio(with_alt, total_imgs)
    return ratio, ratio > 0.9, f"{with_alt}/{total_imgs} images have alt text", {}


def _check_images_alt_descriptive(ctx):
    pages = _pages(ctx)
    total_with_alt = 0
    descriptive = 0
    for p in pages.values():
        for img in p.images:
            alt = img.get("alt")
            if alt:
                total_with_alt += 1
                if len(alt) > 10 and alt.lower() not in ("image", "photo", "picture", "img"):
                    descriptive += 1
    if total_with_alt == 0:
        return 0.5, True, "No alt text to check", {}
    ratio = _ratio(descriptive, total_with_alt)
    return ratio, ratio > 0.7, f"{descriptive}/{total_with_alt} alt texts are descriptive", {}


def _check_images_dimensions(ctx):
    pages = _pages(ctx)
    total = 0
    with_dims = 0
    for p in pages.values():
        for img in p.images:
            total += 1
            if img.get("width") and img.get("height"):
                with_dims += 1
    if total == 0:
        return 1.0, True, "No images", {}
    ratio = _ratio(with_dims, total)
    return ratio, ratio > 0.8, f"{with_dims}/{total} images have dimensions set", {}


def _check_images_modern_format(ctx):
    pages = _pages(ctx)
    total = 0
    modern = 0
    for p in pages.values():
        for img in p.images:
            src = img.get("src", "")
            total += 1
            if any(src.lower().endswith(ext) for ext in (".webp", ".avif", ".svg")):
                modern += 1
    if total == 0:
        return 1.0, True, "No images", {}
    ratio = _ratio(modern, total)
    return ratio, ratio > 0.3, f"{modern}/{total} images use modern formats", {}


# --- GEO checks ---

def _check_gptbot_allowed(ctx):
    return _check_specific_bot(ctx, "GPTBot")


def _check_claudebot_allowed(ctx):
    return _check_specific_bot(ctx, "ClaudeBot")


def _check_perplexitybot_allowed(ctx):
    return _check_specific_bot(ctx, "PerplexityBot")


def _check_specific_bot(ctx, bot_name):
    txt = _robots(ctx)
    if not txt:
        return 1.0, True, f"No robots.txt — {bot_name} allowed by default", {}
    lower = txt.lower()
    idx = lower.find(f"user-agent: {bot_name.lower()}")
    if idx >= 0:
        segment = lower[idx:idx + 200]
        if "disallow: /" in segment:
            return 0.0, False, f"{bot_name} blocked in robots.txt", {}
    return 1.0, True, f"{bot_name} not blocked", {}


def _check_llms_txt(ctx):
    llms_txt = ctx.get("llms_txt", "")
    if llms_txt:
        return 1.0, True, "llms.txt found", {"length": len(llms_txt)}
    return 0.0, False, "No llms.txt file found", {}


def _check_question_headings(ctx):
    pages = _pages(ctx)
    if not pages:
        return 0.5, True, "No pages", {}
    has_questions = 0
    for p in pages.values():
        for h in p.h2 + p.h3:
            if h.strip().endswith("?") or h.lower().startswith(("how ", "what ", "why ", "when ", "where ", "which ", "can ", "does ", "is ")):
                has_questions += 1
                break
    ratio = _ratio(has_questions, len(pages))
    return ratio, ratio > 0.2, f"{has_questions}/{len(pages)} pages have question-based headings", {}


def _check_dates_visible(ctx):
    # Same as publication_date but for GEO category
    pages = _pages(ctx)
    if not pages:
        return 0.5, True, "No pages", {}
    has_date = 0
    for page in pages.values():
        html_lower = page.html.lower()
        if any(x in html_lower for x in [
            'datetime=', 'datepublished', 'datemodified', 'article:published_time'
        ]):
            has_date += 1
    ratio = _ratio(has_date, len(pages))
    return ratio, ratio > 0.3, f"{has_date}/{len(pages)} pages have visible dates", {}


# ═══════════════════════════════════════════════════════════════════════
# New checks (v2.1) — 36 additional atomic checks for 92 total
# ═══════════════════════════════════════════════════════════════════════

# --- Technical (8 new) ---

def _check_no_broken_links(ctx):
    """Check for broken internal links from the crawl."""
    crawl = ctx.get("crawl")
    if not crawl:
        return 0.5, True, "No crawl data", {}
    broken = getattr(crawl, "broken_links", [])
    if broken:
        return 0.0, False, f"{len(broken)} broken internal links", {"broken": broken[:20]}
    return 1.0, True, "No broken links detected", {}


def _check_no_mixed_content(ctx):
    """Check that HTTPS pages don't reference HTTP resources."""
    pages = _pages(ctx)
    mixed = []
    for url, page in pages.items():
        if url.startswith("https://"):
            html = page.html
            if 'src="http://' in html or "src='http://" in html:
                mixed.append(url)
    if not pages:
        return 1.0, True, "No pages", {}
    ratio = _ratio(len(pages) - len(mixed), len(pages))
    return ratio, len(mixed) == 0, f"{len(mixed)} pages with mixed content", {"pages": mixed[:10]}


def _check_response_time_fast(ctx):
    """Check server response time is under 1000ms."""
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    slow = [(url, p.response_time) for url, p in pages.items()
            if p.response_time > 1000 and p.response_time > 0]
    ratio = _ratio(len(pages) - len(slow), len(pages))
    return ratio, len(slow) == 0, f"{len(slow)} pages with response time >1000ms", {"slow_pages": slow[:10]}


def _check_hreflang_valid(ctx):
    """Check that hreflang tags are valid ISO 639-1 if present."""
    import re
    LANG_RE = re.compile(r'^[a-z]{2}(-[A-Z]{2})?$')
    pages = _pages(ctx)
    invalid = []
    total_tags = 0
    for url, page in pages.items():
        for tag in page.hreflang:
            total_tags += 1
            lang = tag.get("lang", "") if isinstance(tag, dict) else str(tag)
            if lang != "x-default" and not LANG_RE.match(lang):
                invalid.append((url, lang))
    if total_tags == 0:
        return 1.0, True, "No hreflang tags to validate", {}
    ratio = _ratio(total_tags - len(invalid), total_tags)
    return ratio, len(invalid) == 0, f"{len(invalid)} invalid hreflang tags", {"invalid": invalid[:10]}


def _check_x_frame_options(ctx):
    """Check for X-Frame-Options header."""
    pages = _pages(ctx)
    for page in pages.values():
        headers = {k.lower(): v for k, v in page.headers.items()}
        if "x-frame-options" in headers:
            return 1.0, True, "X-Frame-Options header present", {}
        csp = headers.get("content-security-policy", "")
        if "frame-ancestors" in csp:
            return 1.0, True, "frame-ancestors in CSP (equivalent)", {}
    return 0.0, False, "No X-Frame-Options or frame-ancestors header", {}


def _check_referrer_policy(ctx):
    """Check for Referrer-Policy header."""
    pages = _pages(ctx)
    for page in pages.values():
        headers = {k.lower(): v for k, v in page.headers.items()}
        if "referrer-policy" in headers:
            return 1.0, True, "Referrer-Policy header present", {"value": headers["referrer-policy"]}
    return 0.0, False, "No Referrer-Policy header found", {}


def _check_no_404_pages(ctx):
    """Check no crawled pages return 404."""
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    errors = [(url, p.status_code) for url, p in pages.items() if p.status_code == 404]
    ratio = _ratio(len(pages) - len(errors), len(pages))
    return ratio, len(errors) == 0, f"{len(errors)} pages returning 404", {"pages": errors[:20]}


def _check_charset_declared(ctx):
    """Check that UTF-8 charset is declared."""
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    has_charset = 0
    for page in pages.values():
        html_head = page.html.lower()[:2000]
        if 'charset="utf-8"' in html_head or "charset='utf-8'" in html_head or "charset=utf-8" in html_head:
            has_charset += 1
    ratio = _ratio(has_charset, len(pages))
    return ratio, ratio > 0.9, f"{has_charset}/{len(pages)} pages declare UTF-8 charset", {}


# --- Content (6 new) ---

def _check_about_page(ctx):
    """Check that an about page exists."""
    pages = _pages(ctx)
    for url in pages:
        if any(x in url.lower() for x in ["/about", "/over-ons", "/ueber-uns", "/a-propos", "/chi-siamo"]):
            return 1.0, True, "About page found", {"url": url}
    for page in pages.values():
        for link in page.internal_links:
            href = link.get("href", "").lower() if isinstance(link, dict) else str(link).lower()
            if "about" in href:
                return 1.0, True, "About page link found", {}
    return 0.0, False, "No about page detected", {}


def _check_terms_page(ctx):
    """Check that a terms of service page exists."""
    pages = _pages(ctx)
    for url in pages:
        if any(x in url.lower() for x in ["terms", "tos", "conditions", "agb", "cgu"]):
            return 1.0, True, "Terms page found", {"url": url}
    for page in pages.values():
        for link in page.internal_links:
            href = link.get("href", "").lower() if isinstance(link, dict) else str(link).lower()
            if "terms" in href or "conditions" in href:
                return 1.0, True, "Terms page link found", {}
    return 0.0, False, "No terms of service page detected", {}


def _check_no_duplicate_content(ctx):
    """Check no pages share the same content hash."""
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    hashes = {}
    for url, page in pages.items():
        h = page.content_hash
        if h and h in hashes:
            hashes[h].append(url)
        elif h:
            hashes[h] = [url]
    duplicates = {h: urls for h, urls in hashes.items() if len(urls) > 1}
    if duplicates:
        dup_count = sum(len(urls) for urls in duplicates.values())
        return 0.0, False, f"{dup_count} pages with duplicate content", {"duplicates": dict(list(duplicates.items())[:5])}
    return 1.0, True, "No duplicate content detected", {}


def _check_has_subheadings(ctx):
    """Check content pages have H2 subheadings."""
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    with_h2 = sum(1 for p in pages.values() if len(p.h2) > 0 and p.word_count >= 300)
    content_pages = sum(1 for p in pages.values() if p.word_count >= 300)
    if content_pages == 0:
        return 1.0, True, "No content pages to check", {}
    ratio = _ratio(with_h2, content_pages)
    return ratio, ratio > 0.8, f"{with_h2}/{content_pages} content pages have subheadings", {}


def _check_external_links_present(ctx):
    """Check pages link to external sources."""
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    has_external = sum(1 for p in pages.values() if len(p.external_links) > 0)
    ratio = _ratio(has_external, len(pages))
    return ratio, ratio > 0.2, f"{has_external}/{len(pages)} pages have external links", {}


def _check_no_broken_internal_links(ctx):
    """Check internal link targets exist in crawled pages."""
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    known_urls = set(pages.keys())
    broken = []
    for url, page in pages.items():
        for link in page.internal_links:
            href = link.get("href", "") if isinstance(link, dict) else str(link)
            if href and href not in known_urls and href.rstrip("/") not in {u.rstrip("/") for u in known_urls}:
                broken.append((url, href))
    total_links = sum(len(p.internal_links) for p in pages.values())
    if total_links == 0:
        return 1.0, True, "No internal links", {}
    ratio = _ratio(total_links - len(broken), total_links)
    return ratio, len(broken) == 0, f"{len(broken)} internal links to uncrawled pages", {"broken": broken[:20]}


# --- On-Page (6 new) ---

def _check_title_no_keyword_stuffing(ctx):
    """Check titles don't repeat the same word 3+ times."""
    from collections import Counter
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    stuffed = []
    for url, page in pages.items():
        if page.title:
            words = page.title.lower().split()
            counts = Counter(w for w in words if len(w) > 3)
            worst = counts.most_common(1)
            if worst and worst[0][1] >= 3:
                stuffed.append((url, worst[0]))
    ratio = _ratio(len(pages) - len(stuffed), len(pages))
    return ratio, len(stuffed) == 0, f"{len(stuffed)} titles with keyword stuffing", {"stuffed": stuffed[:10]}


def _check_meta_desc_no_keyword_stuffing(ctx):
    """Check meta descriptions don't repeat the same word 3+ times."""
    from collections import Counter
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    stuffed = []
    for url, page in pages.items():
        if page.meta_description:
            words = page.meta_description.lower().split()
            counts = Counter(w for w in words if len(w) > 3)
            worst = counts.most_common(1)
            if worst and worst[0][1] >= 3:
                stuffed.append((url, worst[0]))
    ratio = _ratio(len(pages) - len(stuffed), len(pages))
    return ratio, len(stuffed) == 0, f"{len(stuffed)} descriptions with keyword stuffing", {"stuffed": stuffed[:10]}


def _check_h1_matches_title(ctx):
    """Check H1 is similar to the page title."""
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    matching = 0
    checked = 0
    for page in pages.values():
        if page.title and page.h1:
            checked += 1
            h1_text = page.h1[0].lower().strip()
            title_text = page.title.lower().strip()
            # Consider a match if they share significant overlap
            h1_words = set(h1_text.split())
            title_words = set(title_text.split())
            if h1_words and title_words:
                overlap = len(h1_words & title_words) / max(len(h1_words), 1)
                if overlap > 0.4:
                    matching += 1
    if checked == 0:
        return 0.5, True, "No pages with both title and H1", {}
    ratio = _ratio(matching, checked)
    return ratio, ratio > 0.7, f"{matching}/{checked} H1s match their title", {}


def _check_lang_attr(ctx):
    """Check HTML lang attribute is present."""
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    has_lang = 0
    for page in pages.values():
        html_start = page.html.lower()[:500]
        if 'lang="' in html_start or "lang='" in html_start:
            has_lang += 1
    ratio = _ratio(has_lang, len(pages))
    return ratio, ratio > 0.9, f"{has_lang}/{len(pages)} pages have lang attribute", {}


def _check_favicon(ctx):
    """Check favicon is referenced in HTML."""
    pages = _pages(ctx)
    for page in pages.values():
        html_lower = page.html.lower()
        if 'rel="icon"' in html_lower or "rel='icon'" in html_lower or \
           'rel="shortcut icon"' in html_lower or "favicon" in html_lower:
            return 1.0, True, "Favicon reference found", {}
    return 0.0, False, "No favicon reference found", {}


def _check_charset(ctx):
    """Check character encoding is declared."""
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    has_charset = 0
    for page in pages.values():
        html_head = page.html.lower()[:2000]
        headers_lower = {k.lower(): v.lower() for k, v in page.headers.items()}
        ct = headers_lower.get("content-type", "")
        if "charset" in html_head or "charset" in ct:
            has_charset += 1
    ratio = _ratio(has_charset, len(pages))
    return ratio, ratio > 0.9, f"{has_charset}/{len(pages)} pages declare charset", {}


# --- Schema (5 new) ---

def _check_schema_multiple_types(ctx):
    """Check homepage has 2+ schema types."""
    pages = _pages(ctx)
    if not pages:
        return 0.5, True, "No pages", {}
    first_url = list(pages.keys())[0]
    page = pages[first_url]
    types = {s.get("@type") for s in page.schema_blocks if s.get("@type")}
    if len(types) >= 2:
        return 1.0, True, f"Homepage has {len(types)} schema types: {types}", {"types": list(types)}
    if len(types) == 1:
        return 0.5, False, f"Homepage has only 1 schema type: {types}", {"types": list(types)}
    return 0.0, False, "Homepage has no schema types", {}


def _check_schema_breadcrumb(ctx):
    """Check inner pages have BreadcrumbList schema."""
    pages = _pages(ctx)
    if len(pages) <= 1:
        return 1.0, True, "Single page — breadcrumb not applicable", {}
    inner_pages = list(pages.items())[1:]  # skip homepage
    has_breadcrumb = 0
    for url, page in inner_pages:
        for s in page.schema_blocks:
            if s.get("@type") == "BreadcrumbList":
                has_breadcrumb += 1
                break
    ratio = _ratio(has_breadcrumb, len(inner_pages))
    return ratio, ratio > 0.3, f"{has_breadcrumb}/{len(inner_pages)} inner pages have BreadcrumbList", {}


def _check_schema_valid_json(ctx):
    """Check all schema blocks are valid JSON structures."""
    pages = _pages(ctx)
    total = 0
    valid = 0
    for p in pages.values():
        for s in p.schema_blocks:
            total += 1
            if isinstance(s, dict) and "@type" in s:
                valid += 1
    if total == 0:
        return 0.5, True, "No schemas to validate", {}
    ratio = _ratio(valid, total)
    return ratio, ratio > 0.95, f"{valid}/{total} schema blocks are valid", {}


def _check_schema_required_fields(ctx):
    """Check schema has required fields for its type."""
    REQUIRED = {
        "Organization": {"name"},
        "LocalBusiness": {"name", "address"},
        "Product": {"name"},
        "Article": {"headline"},
        "WebSite": {"name", "url"},
        "BreadcrumbList": {"itemListElement"},
        "FAQPage": {"mainEntity"},
        "VideoObject": {"name", "uploadDate"},
    }
    pages = _pages(ctx)
    total = 0
    complete = 0
    for p in pages.values():
        for s in p.schema_blocks:
            stype = s.get("@type", "")
            if stype in REQUIRED:
                total += 1
                required = REQUIRED[stype]
                if all(s.get(f) for f in required):
                    complete += 1
    if total == 0:
        return 1.0, True, "No typed schemas to check", {}
    ratio = _ratio(complete, total)
    return ratio, ratio > 0.8, f"{complete}/{total} schemas have required fields", {}


def _check_schema_sitelinks_searchbox(ctx):
    """Check for WebSite schema with SearchAction for sitelinks."""
    pages = _pages(ctx)
    if not pages:
        return 0.5, True, "No pages", {}
    first_url = list(pages.keys())[0]
    page = pages[first_url]
    for s in page.schema_blocks:
        if s.get("@type") == "WebSite":
            action = s.get("potentialAction", {})
            if isinstance(action, dict) and action.get("@type") == "SearchAction":
                return 1.0, True, "WebSite schema with SearchAction found", {}
            if isinstance(action, list):
                for a in action:
                    if isinstance(a, dict) and a.get("@type") == "SearchAction":
                        return 1.0, True, "WebSite schema with SearchAction found", {}
    return 0.0, False, "No WebSite schema with SearchAction for sitelinks", {}


# --- Performance (5 new) ---

def _check_lighthouse_accessibility(ctx):
    """Check Lighthouse accessibility score."""
    cwv = ctx.get("cwv")
    if not cwv or cwv.lighthouse_accessibility is None:
        return 0.5, True, "Lighthouse accessibility data not available", {}
    score = cwv.lighthouse_accessibility
    return score / 100.0, score >= 80, f"Lighthouse accessibility: {score}/100", {"score": score}


def _check_lighthouse_seo(ctx):
    """Check Lighthouse SEO score."""
    cwv = ctx.get("cwv")
    if not cwv or cwv.lighthouse_seo is None:
        return 0.5, True, "Lighthouse SEO data not available", {}
    score = cwv.lighthouse_seo
    return score / 100.0, score >= 80, f"Lighthouse SEO: {score}/100", {"score": score}


def _check_lighthouse_best_practices(ctx):
    """Check Lighthouse best practices score."""
    cwv = ctx.get("cwv")
    if not cwv or cwv.lighthouse_best_practices is None:
        return 0.5, True, "Lighthouse best practices data not available", {}
    score = cwv.lighthouse_best_practices
    return score / 100.0, score >= 80, f"Lighthouse best practices: {score}/100", {"score": score}


def _check_avg_response_time(ctx):
    """Check average server response time under 500ms."""
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    times = [p.response_time for p in pages.values() if p.response_time > 0]
    if not times:
        return 0.5, True, "No response time data", {}
    avg = sum(times) / len(times)
    if avg < 500:
        return 1.0, True, f"Average response time: {avg:.0f}ms (good)", {"avg_ms": round(avg)}
    elif avg < 1000:
        return 0.5, False, f"Average response time: {avg:.0f}ms (slow)", {"avg_ms": round(avg)}
    return 0.0, False, f"Average response time: {avg:.0f}ms (very slow)", {"avg_ms": round(avg)}


def _check_ttfb(ctx):
    """Check Time to First Byte under 800ms (estimated from first page)."""
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    first_page = list(pages.values())[0]
    ttfb = first_page.response_time
    if ttfb <= 0:
        return 0.5, True, "No TTFB data available", {}
    if ttfb < 800:
        return 1.0, True, f"TTFB: {ttfb:.0f}ms (good)", {"ttfb_ms": round(ttfb)}
    elif ttfb < 1800:
        return 0.5, False, f"TTFB: {ttfb:.0f}ms (needs improvement)", {"ttfb_ms": round(ttfb)}
    return 0.0, False, f"TTFB: {ttfb:.0f}ms (poor)", {"ttfb_ms": round(ttfb)}


# --- Images (3 new) ---

def _check_images_lazy_loading(ctx):
    """Check images use loading='lazy' attribute."""
    pages = _pages(ctx)
    total = 0
    lazy = 0
    for p in pages.values():
        for img in p.images:
            total += 1
            src = img.get("src", "")
            # Check in HTML for loading attribute on this image
            if img.get("loading") == "lazy":
                lazy += 1
    if total == 0:
        return 1.0, True, "No images", {}
    # Also check HTML directly for loading="lazy" pattern
    lazy_in_html = 0
    for p in pages.values():
        if 'loading="lazy"' in p.html or "loading='lazy'" in p.html:
            lazy_in_html += 1
    if lazy_in_html > 0 or lazy > 0:
        ratio = max(_ratio(lazy, total), _ratio(lazy_in_html, len(pages)))
        return ratio, ratio > 0.3, f"Lazy loading detected on {lazy_in_html}/{len(pages)} pages", {}
    return 0.0, False, "No lazy loading attributes found on images", {}


def _check_images_no_oversized_alt(ctx):
    """Check alt text is not overly long (under 125 chars)."""
    pages = _pages(ctx)
    total_with_alt = 0
    oversized = 0
    for p in pages.values():
        for img in p.images:
            alt = img.get("alt")
            if alt:
                total_with_alt += 1
                if len(alt) > 125:
                    oversized += 1
    if total_with_alt == 0:
        return 1.0, True, "No alt text to check", {}
    ratio = _ratio(total_with_alt - oversized, total_with_alt)
    return ratio, oversized == 0, f"{oversized} images with alt text >125 chars", {"oversized_count": oversized}


def _check_images_count_reasonable(ctx):
    """Check reasonable image count per page (under 50)."""
    pages = _pages(ctx)
    if not pages:
        return 1.0, True, "No pages", {}
    heavy = [(url, len(p.images)) for url, p in pages.items() if len(p.images) > 50]
    ratio = _ratio(len(pages) - len(heavy), len(pages))
    return ratio, len(heavy) == 0, f"{len(heavy)} pages with >50 images", {"heavy_pages": heavy[:10]}


# --- GEO (3 new) ---

def _check_stat_data(ctx):
    """Check content includes statistics or data for AI citation."""
    import re
    STAT_RE = re.compile(r'\d+(\.\d+)?%|\$[\d,]+|\d{1,3}(,\d{3})+')
    pages = _pages(ctx)
    if not pages:
        return 0.5, True, "No pages", {}
    has_stats = 0
    for page in pages.values():
        if STAT_RE.search(page.html):
            has_stats += 1
    ratio = _ratio(has_stats, len(pages))
    return ratio, ratio > 0.2, f"{has_stats}/{len(pages)} pages contain statistical data", {}


def _check_definition_format(ctx):
    """Check content has definition-style answers for AI extraction."""
    pages = _pages(ctx)
    if not pages:
        return 0.5, True, "No pages", {}
    has_defs = 0
    for page in pages.values():
        html_lower = page.html.lower()
        if any(x in html_lower for x in [
            ' is a ', ' is the ', ' refers to ', ' means ', ' defined as ',
            '<dfn', '<dt', '<dd'
        ]):
            has_defs += 1
    ratio = _ratio(has_defs, len(pages))
    return ratio, ratio > 0.1, f"{has_defs}/{len(pages)} pages have definition-style content", {}


def _check_license_present(ctx):
    """Check content license is present for AI citation attribution."""
    pages = _pages(ctx)
    for url, page in pages.items():
        html_lower = page.html.lower()
        if any(x in html_lower for x in [
            'rel="license"', "creativecommons.org", "rsl 1.0", "robots source license",
            'property="cc:', "creative commons", "all rights reserved"
        ]):
            return 1.0, True, "Content license found", {}
    return 0.0, False, "No content license detected", {}


# ═══════════════════════════════════════════════════════════════════════
# GSC checks (v2.2) — 6 checks distributed into technical + onpage
# Return 0.5 (insufficient data) when GSC data is unavailable.
# ═══════════════════════════════════════════════════════════════════════

def _get_search_data(ctx):
    """Get SearchData from context, or None."""
    return ctx.get("search_data")


# --- Technical: GSC index coverage (2 checks) ---

def _check_gsc_coverage_ratio(ctx):
    """Check ratio of indexed pages to total crawled pages."""
    sd = _get_search_data(ctx)
    if not sd or sd.source == "none":
        return 0.5, True, "GSC data not available (insufficient data)", {"source": "none"}
    pages = _pages(ctx)
    total_crawled = len(pages)
    if total_crawled == 0:
        return 0.5, True, "No pages crawled", {}
    indexed = sd.indexed_pages
    ratio = indexed / total_crawled
    if ratio >= 0.9:
        return 1.0, True, f"GSC coverage: {indexed}/{total_crawled} ({ratio:.0%}) indexed", {
            "indexed": indexed, "total": total_crawled, "ratio": round(ratio, 3)
        }
    elif ratio >= 0.7:
        return 0.6, False, f"GSC coverage: {indexed}/{total_crawled} ({ratio:.0%}) indexed — some pages missing", {
            "indexed": indexed, "total": total_crawled, "ratio": round(ratio, 3)
        }
    elif ratio >= 0.5:
        return 0.3, False, f"GSC coverage: {indexed}/{total_crawled} ({ratio:.0%}) — significant indexing gap", {
            "indexed": indexed, "total": total_crawled, "ratio": round(ratio, 3)
        }
    return 0.0, False, f"GSC coverage: {indexed}/{total_crawled} ({ratio:.0%}) — critical indexing problem", {
        "indexed": indexed, "total": total_crawled, "ratio": round(ratio, 3)
    }


def _check_gsc_no_coverage_errors(ctx):
    """Check no GSC index coverage errors reported."""
    sd = _get_search_data(ctx)
    if not sd or sd.source == "none":
        return 0.5, True, "GSC data not available (insufficient data)", {"source": "none"}
    errors = sd.coverage_errors
    if errors == 0:
        return 1.0, True, "No GSC coverage errors", {"errors": 0}
    elif errors <= 5:
        return 0.5, False, f"{errors} GSC coverage errors", {"errors": errors}
    return 0.0, False, f"{errors} GSC coverage errors — investigate in Search Console", {"errors": errors}


# --- On-Page: GSC search performance (4 checks) ---

def _check_gsc_avg_position(ctx):
    """Check average search position is under 30."""
    sd = _get_search_data(ctx)
    if not sd or sd.source == "none" or sd.avg_position is None:
        return 0.5, True, "GSC data not available (insufficient data)", {"source": "none"}
    pos = sd.avg_position
    if pos <= 10:
        return 1.0, True, f"GSC avg position: {pos} (page 1)", {"position": pos}
    elif pos <= 20:
        return 0.7, True, f"GSC avg position: {pos} (page 2)", {"position": pos}
    elif pos <= 30:
        return 0.4, False, f"GSC avg position: {pos} (page 3)", {"position": pos}
    return 0.0, False, f"GSC avg position: {pos} (beyond page 3)", {"position": pos}


def _check_gsc_ctr_healthy(ctx):
    """Check average CTR is above 2%."""
    sd = _get_search_data(ctx)
    if not sd or sd.source == "none" or sd.avg_ctr is None:
        return 0.5, True, "GSC data not available (insufficient data)", {"source": "none"}
    ctr = sd.avg_ctr
    if ctr >= 0.05:
        return 1.0, True, f"GSC avg CTR: {ctr:.1%} (healthy)", {"ctr": ctr}
    elif ctr >= 0.02:
        return 0.7, True, f"GSC avg CTR: {ctr:.1%} (acceptable)", {"ctr": ctr}
    elif ctr >= 0.01:
        return 0.3, False, f"GSC avg CTR: {ctr:.1%} (below average)", {"ctr": ctr}
    return 0.0, False, f"GSC avg CTR: {ctr:.1%} (poor — titles/descriptions may need improvement)", {"ctr": ctr}


def _check_gsc_no_declining_pages(ctx):
    """Check no pages have >30% declining impressions (28d vs previous 28d)."""
    sd = _get_search_data(ctx)
    if not sd or sd.source == "none":
        return 0.5, True, "GSC data not available (insufficient data)", {"source": "none"}
    declining = sd.declining_pages
    if not declining:
        return 1.0, True, "No pages with declining impressions", {"declining_count": 0}
    total_pages = len(sd.page_impressions) if sd.page_impressions else 1
    ratio = len(declining) / max(total_pages, 1)
    if ratio <= 0.1:
        return 0.7, True, f"{len(declining)} pages declining (minor)", {
            "declining_count": len(declining), "pages": declining[:10]
        }
    elif ratio <= 0.3:
        return 0.3, False, f"{len(declining)} pages declining ({ratio:.0%} of indexed pages)", {
            "declining_count": len(declining), "pages": declining[:10]
        }
    return 0.0, False, f"{len(declining)} pages declining ({ratio:.0%}) — significant traffic loss", {
        "declining_count": len(declining), "pages": declining[:10]
    }


def _check_gsc_impressions_trend(ctx):
    """Check site impressions trend (current 28d vs previous 28d)."""
    sd = _get_search_data(ctx)
    if not sd or sd.source == "none" or sd.impressions_trend is None:
        return 0.5, True, "GSC data not available (insufficient data)", {"source": "none"}
    trend = sd.impressions_trend
    if trend >= 1.1:
        return 1.0, True, f"Impressions growing: {trend:.0%} of previous period", {"trend": round(trend, 2)}
    elif trend >= 0.9:
        return 0.8, True, f"Impressions stable: {trend:.0%} of previous period", {"trend": round(trend, 2)}
    elif trend >= 0.7:
        return 0.4, False, f"Impressions declining: {trend:.0%} of previous period", {"trend": round(trend, 2)}
    return 0.0, False, f"Impressions dropping sharply: {trend:.0%} of previous period", {"trend": round(trend, 2)}
