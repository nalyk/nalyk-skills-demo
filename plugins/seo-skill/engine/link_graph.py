"""Internal link graph analysis with PageRank-like scoring."""

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Optional

from engine import CrawlResult


@dataclass
class SuggestedLink:
    """A suggested internal link between two pages."""
    source_url: str
    target_url: str
    anchor_text: str
    reason: str
    context: str  # surrounding sentence


@dataclass
class LinkGraphResult:
    """Results from internal link graph analysis."""
    internal_pagerank: dict = field(default_factory=dict)
    orphan_pages: list = field(default_factory=list)
    dead_ends: list = field(default_factory=list)
    hub_pages: list = field(default_factory=list)
    authority_pages: list = field(default_factory=list)
    cannibalization: list = field(default_factory=list)
    suggested_links: list = field(default_factory=list)
    link_equity_summary: dict = field(default_factory=dict)


class LinkGraph:
    """Internal link graph analysis."""

    def analyze(self, crawl: CrawlResult) -> LinkGraphResult:
        """Analyze the internal link graph: PageRank, orphans, hubs, cannibalization."""
        result = LinkGraphResult()

        if not crawl.link_graph:
            return result

        # 1. PageRank
        result.internal_pagerank = self._pagerank(crawl.link_graph)

        # 2. Orphan pages (no incoming links, excluding start URL)
        incoming = defaultdict(int)
        for source, targets in crawl.link_graph.items():
            for target in targets:
                incoming[target] += 1

        result.orphan_pages = [
            url for url in crawl.pages
            if url not in incoming and url != crawl.start_url
        ]

        # 3. Dead ends (no outgoing internal links)
        result.dead_ends = [
            url for url, targets in crawl.link_graph.items()
            if len(targets) == 0
        ]

        # 4. Hub pages (top 10 by outgoing link count)
        outgoing = [(url, len(targets)) for url, targets in crawl.link_graph.items()]
        outgoing.sort(key=lambda x: x[1], reverse=True)
        result.hub_pages = [{"url": url, "outgoing_links": count} for url, count in outgoing[:10]]

        # 5. Authority pages (top 10 by incoming link count)
        auth = [(url, count) for url, count in incoming.items()]
        auth.sort(key=lambda x: x[1], reverse=True)
        result.authority_pages = [{"url": url, "incoming_links": count} for url, count in auth[:10]]

        # 6. Cannibalization detection (pages with similar titles/H1s)
        result.cannibalization = self._detect_cannibalization(crawl)

        # 7. Suggested links
        result.suggested_links = self._suggest_links(crawl)

        # 8. Link equity summary
        pr = result.internal_pagerank
        if pr:
            sorted_pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)
            result.link_equity_summary = {
                "top_5_pages": [{"url": u, "pagerank": round(s, 6)} for u, s in sorted_pr[:5]],
                "bottom_5_pages": [{"url": u, "pagerank": round(s, 6)} for u, s in sorted_pr[-5:]],
                "total_pages": len(pr),
                "orphan_count": len(result.orphan_pages),
                "dead_end_count": len(result.dead_ends),
            }

        return result

    def _pagerank(self, graph: dict, damping: float = 0.85, iterations: int = 50) -> dict:
        """Simplified PageRank for internal link graph."""
        # Collect all nodes
        all_nodes = set(graph.keys())
        for targets in graph.values():
            all_nodes.update(targets)

        N = len(all_nodes)
        if N == 0:
            return {}

        rank = {url: 1.0 / N for url in all_nodes}

        # Build reverse graph for efficiency
        incoming_map = defaultdict(list)
        for source, targets in graph.items():
            outgoing_count = len(targets)
            for target in targets:
                incoming_map[target].append((source, outgoing_count))

        for _ in range(iterations):
            new_rank = {}
            for url in all_nodes:
                incoming_sum = sum(
                    rank[src] / out_count
                    for src, out_count in incoming_map.get(url, [])
                    if out_count > 0
                )
                new_rank[url] = (1 - damping) / N + damping * incoming_sum
            rank = new_rank

        return rank

    def _detect_cannibalization(self, crawl: CrawlResult) -> list:
        """Find pages competing for the same keywords (similar titles/H1s)."""
        results = []
        pages = list(crawl.pages.items())

        for i in range(len(pages)):
            for j in range(i + 1, len(pages)):
                url_a, page_a = pages[i]
                url_b, page_b = pages[j]

                # Compare titles
                title_a = (page_a.title or "").lower().strip()
                title_b = (page_b.title or "").lower().strip()

                if not title_a or not title_b:
                    continue

                # Simple word overlap ratio
                words_a = set(re.findall(r"\w+", title_a))
                words_b = set(re.findall(r"\w+", title_b))
                # Remove stopwords
                stops = {"the", "a", "an", "is", "are", "was", "in", "on", "at", "to", "for",
                         "of", "and", "or", "with", "by", "from", "as", "how", "what", "why"}
                words_a -= stops
                words_b -= stops

                if not words_a or not words_b:
                    continue

                overlap = words_a & words_b
                union = words_a | words_b
                similarity = len(overlap) / len(union)

                if similarity > 0.6:
                    results.append({
                        "url_a": url_a,
                        "url_b": url_b,
                        "title_a": page_a.title,
                        "title_b": page_b.title,
                        "similarity": round(similarity, 2),
                        "overlapping_words": list(overlap),
                    })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:20]

    def _suggest_links(self, crawl: CrawlResult) -> list:
        """Suggest missing internal links based on content relevance."""
        suggestions = []

        # Build keyword → URL map from titles and H1s
        keyword_map = defaultdict(list)
        for url, page in crawl.pages.items():
            keywords = set()
            for text in ([page.title or ""] + page.h1 + page.h2):
                words = re.findall(r"\w{4,}", text.lower())
                keywords.update(words)
            for kw in keywords:
                keyword_map[kw].append(url)

        # For each page, find keywords in content that could link to other pages
        for url, page in crawl.pages.items():
            linked_urls = {
                l.get("href", "") if isinstance(l, dict) else str(l)
                for l in page.internal_links
            }

            # Check if page content mentions keywords from other page titles
            content_lower = page.html.lower()[:50000]

            for keyword, target_urls in keyword_map.items():
                if len(keyword) < 5:
                    continue
                if keyword not in content_lower:
                    continue

                for target_url in target_urls:
                    if target_url == url:
                        continue
                    if target_url in linked_urls:
                        continue

                    target_page = crawl.pages.get(target_url)
                    if not target_page:
                        continue

                    suggestions.append(SuggestedLink(
                        source_url=url,
                        target_url=target_url,
                        anchor_text=target_page.title or keyword,
                        reason=f"Content mentions '{keyword}' which is a key topic of the target page",
                        context=keyword,
                    ))

        # Deduplicate and limit
        seen = set()
        unique = []
        for s in suggestions:
            key = (s.source_url, s.target_url)
            if key not in seen:
                seen.add(key)
                unique.append(s)
        return unique[:50]
