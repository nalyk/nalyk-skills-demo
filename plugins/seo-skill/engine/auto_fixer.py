"""Auto-fix generation engine.

For every detected issue, generate a ready-to-apply fix.
"""

import json
import re
from typing import Optional
from urllib.parse import urlparse

from engine import CheckResult, Fix, FixType, PageData, CrawlResult


class AutoFixer:
    """Generate ready-to-apply fixes for all detected SEO issues."""

    def generate_fixes(self, issues: list[CheckResult], crawl: CrawlResult) -> list[Fix]:
        """Generate ready-to-apply fixes for all failing checks."""
        fixes = []
        for issue in issues:
            if issue.passed:
                continue
            fix = self._generate_fix(issue, crawl)
            if fix:
                fixes.append(fix)
        return fixes

    def _generate_fix(self, issue: CheckResult, crawl: CrawlResult) -> Optional[Fix]:
        dispatch = {
            "onpage.title.exists": self._fix_missing_title,
            "onpage.title.length_ok": self._fix_title_length,
            "onpage.meta_desc.exists": self._fix_missing_meta_desc,
            "onpage.meta_desc.length_ok": self._fix_meta_desc_length,
            "tech.security.hsts": self._fix_hsts,
            "tech.security.csp": self._fix_csp,
            "tech.security.x_content_type": self._fix_x_content_type,
            "tech.crawl.robots_txt_exists": self._fix_robots_txt,
            "tech.crawl.sitemap_exists": self._fix_sitemap,
            "tech.crawl.sitemap_in_robots": self._fix_sitemap_in_robots,
            "tech.structured.no_deprecated_schema": self._fix_deprecated_schema,
            "schema.has_jsonld": self._fix_add_schema,
            "schema.no_placeholder": self._fix_schema_placeholders,
            "images.alt_text.present": self._fix_missing_alt,
            "images.dimensions_set": self._fix_missing_dimensions,
            "geo.llms_txt.exists": self._fix_llms_txt,
            "onpage.og.complete": self._fix_og_tags,
            "tech.mobile.viewport_meta": self._fix_viewport,
            "tech.index.canonical_present": self._fix_canonical,
        }
        handler = dispatch.get(issue.check_id)
        if handler:
            return handler(issue, crawl)
        return None

    # ─── Fix generators ───────────────────────────────────────────────

    def _fix_missing_title(self, issue, crawl):
        examples = []
        for url, page in crawl.pages.items():
            if not page.title:
                content = self._first_meaningful_text(page, 60)
                examples.append(f'  <!-- {url} -->\n  <title>{content}</title>')
                if len(examples) >= 3:
                    break
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.HTML_INJECT,
            description="Add title tags to pages missing them",
            code="\n".join(examples),
            impact="Critical — pages without titles won't rank properly"
        )

    def _fix_title_length(self, issue, crawl):
        examples = []
        for url, page in crawl.pages.items():
            if page.title and (len(page.title) < 30 or len(page.title) > 60):
                truncated = page.title[:57] + "..." if len(page.title) > 60 else page.title
                examples.append(f"  {url}: \"{page.title}\" → \"{truncated}\"")
                if len(examples) >= 5:
                    break
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.CONTENT_EDIT,
            description="Adjust title tags to 30-60 characters",
            code="\n".join(examples),
            impact="Medium — improves click-through rate in SERPs"
        )

    def _fix_missing_meta_desc(self, issue, crawl):
        examples = []
        for url, page in crawl.pages.items():
            if not page.meta_description:
                content = self._first_meaningful_text(page, 155)
                examples.append(
                    f'  <!-- {url} -->\n'
                    f'  <meta name="description" content="{self._escape_html(content)}">'
                )
                if len(examples) >= 3:
                    break
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.HTML_INJECT,
            description="Add meta descriptions to pages missing them",
            code="\n".join(examples),
            impact="Medium — improves CTR in search results"
        )

    def _fix_meta_desc_length(self, issue, crawl):
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.CONTENT_EDIT,
            description="Adjust meta descriptions to 120-160 characters",
            code="Review meta descriptions and ensure they're 120-160 chars with a compelling CTA.",
            impact="Low — Google often rewrites descriptions anyway"
        )

    def _fix_hsts(self, issue, crawl):
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.CONFIG_CHANGE,
            description="Add Strict-Transport-Security header",
            code=(
                "# Nginx:\n"
                "add_header Strict-Transport-Security \"max-age=31536000; includeSubDomains\" always;\n\n"
                "# Apache (.htaccess):\n"
                "Header always set Strict-Transport-Security \"max-age=31536000; includeSubDomains\"\n\n"
                "# Cloudflare:\n"
                "Dashboard → SSL/TLS → Edge Certificates → Enable HSTS"
            ),
            impact="Medium — security signal, prevents protocol downgrade attacks"
        )

    def _fix_csp(self, issue, crawl):
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.CONFIG_CHANGE,
            description="Add Content-Security-Policy header",
            code=(
                "# Start with report-only to avoid breaking things:\n"
                "# Nginx:\n"
                "add_header Content-Security-Policy-Report-Only \"default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https:; style-src 'self' 'unsafe-inline' https:; "
                "img-src 'self' data: https:;\" always;\n\n"
                "# Once validated, change to enforcing:\n"
                "add_header Content-Security-Policy \"default-src 'self'; ...\" always;"
            ),
            impact="Low — security improvement, not a direct ranking factor"
        )

    def _fix_x_content_type(self, issue, crawl):
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.CONFIG_CHANGE,
            description="Add X-Content-Type-Options header",
            code=(
                "# Nginx:\n"
                "add_header X-Content-Type-Options \"nosniff\" always;\n\n"
                "# Apache:\n"
                "Header always set X-Content-Type-Options \"nosniff\""
            ),
            impact="Low — prevents MIME-type sniffing attacks"
        )

    def _fix_robots_txt(self, issue, crawl):
        parsed = urlparse(crawl.start_url)
        sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
        return Fix(
            issue_id=issue.check_id, file_path="robots.txt", fix_type=FixType.FILE_CREATE,
            description="Create robots.txt with recommended AI crawler settings",
            code=(
                f"# robots.txt for {parsed.netloc}\n"
                "# Generated by Claude SEO v2\n\n"
                "User-agent: *\n"
                "Allow: /\n\n"
                "# Allow AI search crawlers for visibility\n"
                "User-agent: GPTBot\n"
                "Allow: /\n\n"
                "User-agent: ChatGPT-User\n"
                "Allow: /\n\n"
                "User-agent: ClaudeBot\n"
                "Allow: /\n\n"
                "User-agent: PerplexityBot\n"
                "Allow: /\n\n"
                "# Block AI training-only crawlers (optional)\n"
                "# User-agent: CCBot\n"
                "# Disallow: /\n\n"
                "# User-agent: Google-Extended\n"
                "# Disallow: /\n\n"
                f"Sitemap: {sitemap_url}\n"
            ),
            apply_command="cp robots.txt /path/to/webroot/robots.txt",
            impact="Critical — without robots.txt, crawlers have no guidance"
        )

    def _fix_sitemap(self, issue, crawl):
        urls = list(crawl.pages.keys())[:100]
        entries = "\n".join(
            f"  <url>\n    <loc>{url}</loc>\n  </url>"
            for url in urls
        )
        return Fix(
            issue_id=issue.check_id, file_path="sitemap.xml", fix_type=FixType.FILE_CREATE,
            description="Generate XML sitemap from crawled pages",
            code=(
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                f'{entries}\n'
                '</urlset>'
            ),
            impact="High — helps search engines discover and index all pages"
        )

    def _fix_sitemap_in_robots(self, issue, crawl):
        parsed = urlparse(crawl.start_url)
        return Fix(
            issue_id=issue.check_id, file_path="robots.txt", fix_type=FixType.CONTENT_EDIT,
            description="Add Sitemap directive to robots.txt",
            code=f"\nSitemap: {parsed.scheme}://{parsed.netloc}/sitemap.xml\n",
            impact="Low — helps crawlers discover sitemap automatically"
        )

    def _fix_deprecated_schema(self, issue, crawl):
        found = issue.evidence.get("found", [])
        examples = []
        for url, schema_type in found[:3]:
            if schema_type == "HowTo":
                examples.append(
                    f"  {url}: Replace HowTo schema (deprecated Sept 2023) with Article schema\n"
                    f"  containing step-by-step content in the articleBody."
                )
            elif schema_type == "SpecialAnnouncement":
                examples.append(
                    f"  {url}: Remove SpecialAnnouncement schema (deprecated July 2025).\n"
                    f"  Use Article or NewsArticle schema instead."
                )
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.CONTENT_EDIT,
            description="Replace deprecated schema types",
            code="\n".join(examples) if examples else "Remove deprecated schema types from affected pages.",
            impact="High — deprecated schema won't generate rich results and may confuse crawlers"
        )

    def _fix_add_schema(self, issue, crawl):
        # Generate Organization schema from homepage
        parsed = urlparse(crawl.start_url)
        homepage = crawl.pages.get(crawl.start_url)
        site_name = homepage.title.split("|")[0].strip() if homepage and homepage.title else parsed.netloc

        schema = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": site_name,
            "url": crawl.start_url,
            "sameAs": [],
        }
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.HTML_INJECT,
            description="Add Organization JSON-LD schema to homepage",
            code=(
                f'<script type="application/ld+json">\n'
                f'{json.dumps(schema, indent=2)}\n'
                f'</script>'
            ),
            impact="Medium — helps search engines understand your brand entity"
        )

    def _fix_schema_placeholders(self, issue, crawl):
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.CONTENT_EDIT,
            description="Replace placeholder text in schema markup with real data",
            code="Search for [Business Name], [City], [Phone], etc. in your schema and replace with actual values.",
            impact="Critical — placeholder text in schema renders it useless"
        )

    def _fix_missing_alt(self, issue, crawl):
        examples = []
        for url, page in crawl.pages.items():
            for img in page.images:
                if not img.get("alt"):
                    src = img.get("src", "")
                    filename = src.split("/")[-1].split("?")[0] if src else "image"
                    # Generate descriptive alt from filename
                    alt = re.sub(r"[-_.]", " ", filename).replace("  ", " ").strip()
                    alt = re.sub(r"\.(jpg|jpeg|png|gif|webp|avif|svg)$", "", alt, flags=re.I)
                    if alt and len(alt) > 3:
                        examples.append(f'  <img src="{src}" alt="{alt}">')
                    if len(examples) >= 5:
                        break
            if len(examples) >= 5:
                break
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.CONTENT_EDIT,
            description="Add descriptive alt text to images",
            code="\n".join(examples) if examples else "Add alt attributes to all <img> elements.",
            impact="High — required for accessibility and image SEO"
        )

    def _fix_missing_dimensions(self, issue, crawl):
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.CONTENT_EDIT,
            description="Add width and height attributes to images to prevent CLS",
            code=(
                "Add explicit width and height attributes to all <img> tags:\n"
                '  <img src="photo.jpg" width="800" height="600" alt="Description">\n\n'
                "Or use CSS aspect-ratio as an alternative:\n"
                '  <img src="photo.jpg" style="aspect-ratio: 4/3" alt="Description">'
            ),
            impact="Medium — prevents Cumulative Layout Shift (CLS)"
        )

    def _fix_llms_txt(self, issue, crawl):
        parsed = urlparse(crawl.start_url)
        homepage = crawl.pages.get(crawl.start_url)
        site_name = homepage.title if homepage and homepage.title else parsed.netloc

        # Build page list from crawl
        page_entries = []
        for url, page in list(crawl.pages.items())[:20]:
            title = page.title or urlparse(url).path
            page_entries.append(f"- [{title}]({url})")

        return Fix(
            issue_id=issue.check_id, file_path="llms.txt", fix_type=FixType.FILE_CREATE,
            description="Create llms.txt for AI crawler guidance",
            code=(
                f"# {site_name}\n"
                f"> Official website for {site_name}\n\n"
                f"## Main Pages\n"
                + "\n".join(page_entries) + "\n"
            ),
            apply_command="cp llms.txt /path/to/webroot/llms.txt",
            impact="Medium — helps AI systems understand your site structure"
        )

    def _fix_og_tags(self, issue, crawl):
        examples = []
        for url, page in crawl.pages.items():
            if not page.open_graph.get("og:title"):
                title = page.title or ""
                desc = page.meta_description or ""
                examples.append(
                    f'  <!-- {url} -->\n'
                    f'  <meta property="og:title" content="{self._escape_html(title)}">\n'
                    f'  <meta property="og:description" content="{self._escape_html(desc)}">\n'
                    f'  <meta property="og:url" content="{url}">\n'
                    f'  <meta property="og:type" content="website">'
                )
                if len(examples) >= 2:
                    break
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.HTML_INJECT,
            description="Add Open Graph meta tags",
            code="\n\n".join(examples),
            impact="Low — improves social media sharing previews"
        )

    def _fix_viewport(self, issue, crawl):
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.HTML_INJECT,
            description="Add viewport meta tag for mobile",
            code='<meta name="viewport" content="width=device-width, initial-scale=1">',
            impact="Critical — required for mobile-first indexing"
        )

    def _fix_canonical(self, issue, crawl):
        examples = []
        for url, page in crawl.pages.items():
            if not page.canonical:
                examples.append(f'  <!-- {url} -->\n  <link rel="canonical" href="{page.final_url}">')
                if len(examples) >= 3:
                    break
        return Fix(
            issue_id=issue.check_id, file_path=None, fix_type=FixType.HTML_INJECT,
            description="Add self-referencing canonical tags",
            code="\n\n".join(examples),
            impact="High — prevents duplicate content issues"
        )

    # ─── Helpers ──────────────────────────────────────────────────────

    def _first_meaningful_text(self, page: PageData, max_len: int) -> str:
        """Extract first meaningful text from page for auto-generated meta."""
        if page.h1:
            text = page.h1[0]
        elif page.title:
            text = page.title
        else:
            html = page.html or ""
            text = re.sub(r"<[^>]+>", " ", html[:2000])
            text = re.sub(r"\s+", " ", text).strip()
        if not text:
            text = "Untitled Page"
        return text[:max_len].strip()

    @staticmethod
    def _escape_html(text: str) -> str:
        return text.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
