"""Claude SEO v2 — Deterministic SEO Measurement Engine.

Core data structures and scoring engine for reproducible SEO audits.
"""

__version__ = "2.0.0"

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class Severity(str, Enum):
    """SEO issue severity levels for prioritization."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FixType(str, Enum):
    """Types of auto-generated fixes."""
    HTML_INJECT = "html_inject"
    FILE_CREATE = "file_create"
    CONFIG_CHANGE = "config_change"
    CONTENT_EDIT = "content_edit"


@dataclass
class CheckResult:
    """Single atomic, deterministic check result."""
    check_id: str
    passed: bool
    score: float              # 0.0 to 1.0
    weight: float
    severity: Severity
    message: str
    fix: Optional[str] = None
    evidence: dict = field(default_factory=dict)


@dataclass
class CategoryScore:
    """Aggregated category score with full audit trail."""
    category: str
    score: float              # 0-100, deterministic
    checks: list = field(default_factory=list)
    weight: float = 0.0


@dataclass
class Fix:
    """Ready-to-apply fix for a detected issue."""
    issue_id: str
    file_path: Optional[str]
    fix_type: FixType
    description: str
    code: str
    apply_command: Optional[str] = None
    impact: str = ""


@dataclass
class PageData:
    """Data extracted from a single crawled page."""
    url: str
    final_url: str
    status_code: int
    html: str
    headers: dict
    title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_robots: Optional[str] = None
    canonical: Optional[str] = None
    h1: list = field(default_factory=list)
    h2: list = field(default_factory=list)
    h3: list = field(default_factory=list)
    images: list = field(default_factory=list)
    internal_links: list = field(default_factory=list)
    external_links: list = field(default_factory=list)
    schema_blocks: list = field(default_factory=list)
    open_graph: dict = field(default_factory=dict)
    twitter_card: dict = field(default_factory=dict)
    hreflang: list = field(default_factory=list)
    word_count: int = 0
    redirect_chain: list = field(default_factory=list)
    response_time: float = 0.0
    content_hash: str = ""


@dataclass
class CrawlResult:
    """Complete crawl output."""
    start_url: str
    pages: dict = field(default_factory=dict)       # url -> PageData
    link_graph: dict = field(default_factory=dict)   # url -> set[url]
    redirect_map: dict = field(default_factory=dict)
    broken_links: list = field(default_factory=list)
    orphan_pages: set = field(default_factory=set)
    robots_txt: Optional[str] = None
    robots_rules: dict = field(default_factory=dict)
    sitemap_urls: set = field(default_factory=set)
    pages_crawled: int = 0
    crawl_duration: float = 0.0


@dataclass
class CWVData:
    """Core Web Vitals measurement from PageSpeed Insights."""
    lcp_ms: Optional[float] = None
    inp_ms: Optional[float] = None
    cls: Optional[float] = None
    lcp_rating: str = "unknown"     # good | needs-improvement | poor
    inp_rating: str = "unknown"
    cls_rating: str = "unknown"
    lighthouse_performance: Optional[float] = None
    lighthouse_accessibility: Optional[float] = None
    lighthouse_seo: Optional[float] = None
    lighthouse_best_practices: Optional[float] = None
    opportunities: list = field(default_factory=list)
    source: str = "none"            # field | lab | none


@dataclass
class SearchData:
    """Google Search Console data snapshot for deterministic scoring.

    All metrics are from a fixed date range to ensure reproducibility.
    Score 0.5 (insufficient data) is used when data is unavailable.
    """
    total_pages: int = 0
    indexed_pages: int = 0
    coverage_errors: int = 0
    coverage_warnings: int = 0
    avg_position: Optional[float] = None
    avg_ctr: Optional[float] = None
    total_impressions: int = 0
    total_clicks: int = 0
    page_impressions: dict = field(default_factory=dict)  # url -> impressions
    page_positions: dict = field(default_factory=dict)     # url -> avg position
    page_ctr: dict = field(default_factory=dict)           # url -> ctr
    declining_pages: list = field(default_factory=list)     # urls with declining impressions
    impressions_trend: Optional[float] = None               # ratio: current_period / previous_period
    date_range: str = ""
    source: str = "none"  # gsc | none


@dataclass
class SiteCheckResult:
    """Site-level check result (vs page-level CheckResult).

    Used for metrics that apply to the whole site, not individual pages
    (e.g., GSC coverage ratio, average position across all pages).
    Aggregated into category scores alongside page-level CheckResults.
    """
    check_id: str
    passed: bool
    score: float              # 0.0 to 1.0
    weight: float
    severity: Severity
    message: str
    scope: str = "site"       # always "site" for this type
    fix: Optional[str] = None
    evidence: dict = field(default_factory=dict)


@dataclass
class AuditResult:
    """Complete audit with reproducible scoring."""
    url: str
    timestamp: str
    overall_score: float
    categories: list = field(default_factory=list)
    pages_crawled: int = 0
    issues: list = field(default_factory=list)
    fixes: list = field(default_factory=list)
    comparison: Optional[dict] = None
    crawl_result: Optional[CrawlResult] = None
    cwv_data: Optional[CWVData] = None
    search_data: Optional[SearchData] = None
