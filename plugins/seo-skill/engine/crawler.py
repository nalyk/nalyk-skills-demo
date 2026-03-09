"""Async multi-page SEO spider with link extraction and robots.txt obedience."""

import asyncio
import hashlib
import ipaddress
import json
import re
import socket
import time
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

try:
    import aiohttp
except ImportError:
    aiohttp = None

import requests
from bs4 import BeautifulSoup

from engine import PageData, CrawlResult

try:
    import lxml  # noqa: F401
    _HTML_PARSER = "lxml"
except ImportError:
    _HTML_PARSER = "html.parser"


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ClaudeSEO/2.0; +https://github.com/claude-seo-v2)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

AI_CRAWLERS = ["GPTBot", "ClaudeBot", "PerplexityBot", "ChatGPT-User",
               "OAI-SearchBot", "Bytespider", "Google-Extended", "CCBot",
               "anthropic-ai", "cohere-ai"]


class SEOCrawler:
    """Async multi-page spider with SEO-focused extraction."""

    def __init__(
        self,
        max_pages: int = 200,
        max_depth: int = 5,
        concurrent: int = 10,
        delay: float = 0.5,
        respect_robots: bool = True,
        timeout: int = 30,
    ):
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.concurrent = concurrent
        self.delay = delay
        self.respect_robots = respect_robots
        self.timeout = timeout

    def crawl(self, start_url: str) -> CrawlResult:
        """Synchronous entry point — runs async crawl internally."""
        if aiohttp is None:
            return self._crawl_sync(start_url)
        return asyncio.run(self._crawl_async(start_url))

    # ─── Async implementation ─────────────────────────────────────────

    async def _crawl_async(self, start_url: str) -> CrawlResult:
        parsed = urlparse(start_url)
        base_domain = parsed.netloc
        start_time = time.time()

        result = CrawlResult(start_url=start_url)

        # Fetch robots.txt
        robots_url = f"{parsed.scheme}://{base_domain}/robots.txt"
        result.robots_txt = await self._fetch_text(robots_url)
        result.robots_rules = self._parse_robots_rules(result.robots_txt or "")

        # Fetch sitemap
        sitemap_url = self._extract_sitemap_url(result.robots_txt, parsed)
        if sitemap_url:
            sitemap_content = await self._fetch_text(sitemap_url)
            if sitemap_content:
                result.sitemap_urls = self._parse_sitemap(sitemap_content)

        # Fetch llms.txt
        llms_url = f"{parsed.scheme}://{base_domain}/llms.txt"
        llms_txt = await self._fetch_text(llms_url)

        # BFS crawl
        visited = set()
        queue = asyncio.Queue()
        await queue.put((start_url, 0))

        connector = aiohttp.TCPConnector(limit=self.concurrent, ssl=False)
        async with aiohttp.ClientSession(
            headers=DEFAULT_HEADERS, connector=connector,
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        ) as session:
            while not queue.empty() and len(result.pages) < self.max_pages:
                tasks = []
                batch_size = min(self.concurrent, self.max_pages - len(result.pages))

                for _ in range(batch_size):
                    if queue.empty():
                        break
                    url, depth = await queue.get()
                    if url in visited or depth > self.max_depth:
                        continue
                    if not self._same_domain(url, base_domain):
                        continue
                    visited.add(url)
                    tasks.append(self._fetch_and_parse(session, url, depth))

                if not tasks:
                    break

                pages = await asyncio.gather(*tasks, return_exceptions=True)

                for page_result in pages:
                    if isinstance(page_result, Exception):
                        continue
                    if page_result is None:
                        continue

                    page_data, depth, new_links = page_result
                    result.pages[page_data.url] = page_data

                    # Build link graph
                    targets = set()
                    for link in page_data.internal_links:
                        href = link.get("href", "") if isinstance(link, dict) else str(link)
                        if href and self._same_domain(href, base_domain):
                            targets.add(href)
                            if href not in visited and depth + 1 <= self.max_depth:
                                await queue.put((href, depth + 1))
                    result.link_graph[page_data.url] = targets

                    # Track redirects
                    if page_data.redirect_chain:
                        result.redirect_map[page_data.url] = page_data.final_url

                    # Track broken links
                    if page_data.status_code >= 400:
                        result.broken_links.append({
                            "url": page_data.url,
                            "status": page_data.status_code,
                        })

                if self.delay > 0:
                    await asyncio.sleep(self.delay)

        # Detect orphan pages (in sitemap but not linked)
        linked_pages = set()
        for targets in result.link_graph.values():
            linked_pages.update(targets)
        linked_pages.add(start_url)

        if result.sitemap_urls:
            for sitemap_url in result.sitemap_urls:
                if sitemap_url not in linked_pages and sitemap_url not in result.pages:
                    result.orphan_pages.add(sitemap_url)

        result.pages_crawled = len(result.pages)
        result.crawl_duration = time.time() - start_time

        return result

    async def _fetch_and_parse(self, session, url, depth):
        """Fetch a single page and extract SEO data."""
        start_time = time.time()
        try:
            async with session.get(url, allow_redirects=True, max_redirects=5) as resp:
                html = await resp.text(errors="replace")
                headers = dict(resp.headers)
                status = resp.status
                final_url = str(resp.url)
                redirect_chain = [str(h.url) for h in resp.history] if resp.history else []
        except Exception:
            return None

        response_time = time.time() - start_time
        page_data = self._parse_page(url, final_url, status, html, headers,
                                     redirect_chain, response_time)
        new_links = [l.get("href", "") if isinstance(l, dict) else str(l)
                     for l in page_data.internal_links]
        return page_data, depth, new_links

    async def _fetch_text(self, url: str) -> Optional[str]:
        """Fetch a text resource (robots.txt, sitemap, llms.txt)."""
        if aiohttp is None:
            return self._fetch_text_sync(url)
        try:
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(
                headers=DEFAULT_HEADERS, connector=connector,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        return await resp.text(errors="replace")
        except Exception:
            pass
        return None

    # ─── Sync fallback (no aiohttp) ──────────────────────────────────

    def _crawl_sync(self, start_url: str) -> CrawlResult:
        """Synchronous fallback when aiohttp is not available."""
        parsed = urlparse(start_url)
        base_domain = parsed.netloc
        start_time = time.time()

        result = CrawlResult(start_url=start_url)

        # Fetch robots.txt
        robots_url = f"{parsed.scheme}://{base_domain}/robots.txt"
        result.robots_txt = self._fetch_text_sync(robots_url)
        result.robots_rules = self._parse_robots_rules(result.robots_txt or "")

        # Fetch sitemap
        sitemap_url = self._extract_sitemap_url(result.robots_txt, parsed)
        if sitemap_url:
            sitemap_content = self._fetch_text_sync(sitemap_url)
            if sitemap_content:
                result.sitemap_urls = self._parse_sitemap(sitemap_content)

        # BFS crawl (sync)
        visited = set()
        queue = [(start_url, 0)]

        while queue and len(result.pages) < self.max_pages:
            url, depth = queue.pop(0)
            if url in visited or depth > self.max_depth:
                continue
            if not self._same_domain(url, base_domain):
                continue
            visited.add(url)

            page_data = self._fetch_sync(url)
            if page_data is None:
                continue

            result.pages[page_data.url] = page_data

            targets = set()
            for link in page_data.internal_links:
                href = link.get("href", "") if isinstance(link, dict) else str(link)
                if href and self._same_domain(href, base_domain):
                    targets.add(href)
                    if href not in visited:
                        queue.append((href, depth + 1))
            result.link_graph[page_data.url] = targets

            if page_data.redirect_chain:
                result.redirect_map[page_data.url] = page_data.final_url
            if page_data.status_code >= 400:
                result.broken_links.append({"url": page_data.url, "status": page_data.status_code})

            if self.delay > 0:
                time.sleep(self.delay)

        result.pages_crawled = len(result.pages)
        result.crawl_duration = time.time() - start_time
        return result

    def _fetch_sync(self, url: str) -> Optional[PageData]:
        """Sync single page fetch."""
        # SSRF protection
        try:
            parsed = urlparse(url)
            resolved_ip = socket.gethostbyname(parsed.hostname)
            ip = ipaddress.ip_address(resolved_ip)
            if ip.is_private or ip.is_loopback or ip.is_reserved:
                return None
        except (socket.gaierror, ValueError):
            pass

        try:
            resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=self.timeout,
                                allow_redirects=True)
            redirect_chain = [r.url for r in resp.history] if resp.history else []
            return self._parse_page(url, resp.url, resp.status_code, resp.text,
                                    dict(resp.headers), redirect_chain, resp.elapsed.total_seconds())
        except Exception:
            return None

    def _fetch_text_sync(self, url: str) -> Optional[str]:
        """Sync text fetch."""
        try:
            resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
            if resp.status_code == 200:
                return resp.text
        except Exception:
            pass
        return None

    # ─── HTML parsing ─────────────────────────────────────────────────

    def _parse_page(self, url, final_url, status, html, headers,
                    redirect_chain, response_time) -> PageData:
        """Extract SEO data from HTML."""
        soup = BeautifulSoup(html, _HTML_PARSER)
        parsed_base = urlparse(final_url)
        base_url = f"{parsed_base.scheme}://{parsed_base.netloc}"
        base_domain = parsed_base.netloc

        page = PageData(
            url=url,
            final_url=final_url,
            status_code=status,
            html=html,
            headers=headers,
            redirect_chain=redirect_chain,
            response_time=response_time,
        )

        # Title
        title_tag = soup.find("title")
        if title_tag:
            page.title = title_tag.get_text(strip=True)

        # Meta tags
        for meta in soup.find_all("meta"):
            name = meta.get("name", "").lower()
            prop = meta.get("property", "").lower()
            content = meta.get("content", "")
            if name == "description":
                page.meta_description = content
            elif name == "robots":
                page.meta_robots = content
            if prop.startswith("og:"):
                page.open_graph[prop] = content
            if name.startswith("twitter:"):
                page.twitter_card[name] = content

        # Canonical
        canonical = soup.find("link", rel="canonical")
        if canonical:
            page.canonical = canonical.get("href")

        # Hreflang
        for link in soup.find_all("link", rel="alternate"):
            hl = link.get("hreflang")
            if hl:
                page.hreflang.append({"lang": hl, "href": link.get("href")})

        # Headings
        for tag in ["h1", "h2", "h3"]:
            for h in soup.find_all(tag):
                text = h.get_text(strip=True)
                if text:
                    getattr(page, tag).append(text)

        # Images
        for img in soup.find_all("img"):
            src = img.get("src", "")
            if src:
                src = urljoin(final_url, src)
            page.images.append({
                "src": src,
                "alt": img.get("alt"),
                "width": img.get("width"),
                "height": img.get("height"),
                "loading": img.get("loading"),
            })

        # Links
        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            if not href or href.startswith("#") or href.startswith("javascript:"):
                continue
            full = urljoin(final_url, href)
            link_data = {"href": full, "text": a.get_text(strip=True)[:100]}
            link_parsed = urlparse(full)
            if link_parsed.netloc == base_domain:
                page.internal_links.append(link_data)
            else:
                page.external_links.append(link_data)

        # Schema (JSON-LD)
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    page.schema_blocks.extend(data)
                else:
                    page.schema_blocks.append(data)
            except (json.JSONDecodeError, TypeError):
                pass

        # Word count
        for elem in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            elem.decompose()
        text = soup.get_text(separator=" ", strip=True)
        page.word_count = len(re.findall(r"\b\w+\b", text))

        # Content hash for dedup
        page.content_hash = hashlib.md5(text.encode()).hexdigest()

        return page

    # ─── Helpers ──────────────────────────────────────────────────────

    def _same_domain(self, url: str, base_domain: str) -> bool:
        try:
            return urlparse(url).netloc == base_domain
        except Exception:
            return False

    def _extract_sitemap_url(self, robots_txt: Optional[str], parsed) -> Optional[str]:
        if robots_txt:
            for line in robots_txt.split("\n"):
                if line.strip().lower().startswith("sitemap:"):
                    return line.split(":", 1)[1].strip()
        return f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"

    def _parse_sitemap(self, content: str) -> set:
        urls = set()
        soup = BeautifulSoup(content, "xml" if "lxml" in _HTML_PARSER else _HTML_PARSER)
        for loc in soup.find_all("loc"):
            url = loc.get_text(strip=True)
            if url:
                urls.add(url)
        return urls

    def _parse_robots_rules(self, txt: str) -> dict:
        rules = {"ai_crawlers_blocked": [], "ai_crawlers_allowed": []}
        lower = txt.lower()
        for bot in AI_CRAWLERS:
            idx = lower.find(f"user-agent: {bot.lower()}")
            if idx >= 0:
                segment = lower[idx:idx + 300]
                if "disallow: /" in segment:
                    rules["ai_crawlers_blocked"].append(bot)
                else:
                    rules["ai_crawlers_allowed"].append(bot)
            else:
                rules["ai_crawlers_allowed"].append(bot)
        return rules


if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    crawler = SEOCrawler(max_pages=50, concurrent=5)
    result = crawler.crawl(url)
    print(f"Crawled {result.pages_crawled} pages in {result.crawl_duration:.1f}s")
    print(f"Broken links: {len(result.broken_links)}")
    print(f"Orphan pages: {len(result.orphan_pages)}")
