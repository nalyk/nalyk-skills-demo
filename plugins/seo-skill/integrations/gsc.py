"""Google Search Console integration for Claude SEO v2.

Fetches real search performance and index coverage data via GSC API.
Uses google-api-python-client for pagination, retry, and typed errors.
All dependencies are optional — engine degrades gracefully without them.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlparse

from engine import SearchData


def _resolve_credentials(explicit_path: Optional[str] = None):
    """4-level credential resolution: explicit path -> env var -> ADC -> None.

    Returns a google.oauth2 Credentials object or None.
    Prints which level was used (or all levels attempted on failure).
    """
    levels_attempted = []

    # Level 1: Explicit path
    if explicit_path:
        levels_attempted.append(f"explicit path: {explicit_path}")
        if os.path.isfile(explicit_path):
            try:
                from google.oauth2 import service_account
                creds = service_account.Credentials.from_service_account_file(
                    explicit_path,
                    scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
                )
                return creds
            except Exception as e:
                print(f"   ! GSC credential file found but invalid: {e}", file=sys.stderr)
        else:
            print(f"   ! GSC credential file not found: {explicit_path}", file=sys.stderr)

    # Level 2: Environment variable
    env_path = os.environ.get("GSC_CREDENTIALS")
    if env_path:
        levels_attempted.append(f"env GSC_CREDENTIALS: {env_path}")
        if os.path.isfile(env_path):
            try:
                from google.oauth2 import service_account
                creds = service_account.Credentials.from_service_account_file(
                    env_path,
                    scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
                )
                return creds
            except Exception as e:
                print(f"   ! GSC env credential invalid: {e}", file=sys.stderr)

    # Level 3: Application Default Credentials (ADC)
    levels_attempted.append("Google ADC (gcloud auth)")
    try:
        import google.auth
        creds, _ = google.auth.default(
            scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
        )
        return creds
    except Exception:
        pass

    # All levels failed
    if levels_attempted:
        print(f"   ! GSC auth failed. Attempted: {'; '.join(levels_attempted)}", file=sys.stderr)
    return None


def _match_property(service, site_url: str, explicit_property: Optional[str] = None) -> Optional[str]:
    """Match the audited URL to a GSC property.

    If explicit_property is given, use it directly. Otherwise, try to
    auto-detect from the list of verified properties.
    """
    if explicit_property:
        return explicit_property

    try:
        site_list = service.sites().list().execute()
        sites = site_list.get("siteEntry", [])
    except Exception as e:
        print(f"   ! Failed to list GSC properties: {e}", file=sys.stderr)
        return None

    parsed = urlparse(site_url)
    domain = parsed.netloc.lower().lstrip("www.")

    # Try exact URL property match first
    for site in sites:
        perm = site.get("permissionLevel", "")
        if perm in ("siteUnverifiedUser",):
            continue
        site_id = site.get("siteUrl", "")
        if site_url.startswith(site_id.rstrip("/")):
            return site_id

    # Try domain property match
    for site in sites:
        site_id = site.get("siteUrl", "")
        if site_id.startswith("sc-domain:"):
            prop_domain = site_id.replace("sc-domain:", "").lower()
            if domain == prop_domain or domain.endswith("." + prop_domain):
                return site_id

    # Try URL prefix match
    for site in sites:
        site_id = site.get("siteUrl", "")
        site_domain = urlparse(site_id).netloc.lower().lstrip("www.")
        if domain == site_domain:
            return site_id

    return None


class GSCClient:
    """Google Search Console API client.

    Fetches search analytics and index coverage data for deterministic scoring.
    Returns SearchData dataclass with all metrics needed by the 6 GSC checks.
    """

    def __init__(self, credentials_path: Optional[str] = None,
                 gsc_property: Optional[str] = None,
                 date_range_days: int = 28):
        self.credentials_path = credentials_path
        self.gsc_property = gsc_property
        self.date_range_days = date_range_days

    def fetch(self, site_url: str) -> Optional[SearchData]:
        """Fetch GSC data for the given site URL.

        Returns SearchData or None if GSC is unavailable/unconfigured.
        """
        try:
            from googleapiclient.discovery import build
            from googleapiclient.errors import HttpError
        except ImportError:
            return None

        creds = _resolve_credentials(self.credentials_path)
        if not creds:
            return None

        try:
            service = build("searchconsole", "v1", credentials=creds)
        except Exception as e:
            print(f"   ! Failed to build GSC service: {e}", file=sys.stderr)
            return None

        prop = _match_property(service, site_url, self.gsc_property)
        if not prop:
            print(f"   ! No GSC property found for {site_url}", file=sys.stderr)
            return None

        # Date ranges: current 28d and previous 28d for trend comparison
        end_date = datetime.now() - timedelta(days=3)  # GSC data has 2-3 day lag
        start_date = end_date - timedelta(days=self.date_range_days)
        prev_end = start_date - timedelta(days=1)
        prev_start = prev_end - timedelta(days=self.date_range_days)

        date_str = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"

        search_data = SearchData(date_range=date_str, source="gsc")

        # Fetch search analytics (current period)
        try:
            current = self._fetch_search_analytics(
                service, prop,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
            )
            if current:
                search_data.total_impressions = current["total_impressions"]
                search_data.total_clicks = current["total_clicks"]
                search_data.avg_position = current["avg_position"]
                search_data.avg_ctr = current["avg_ctr"]
                search_data.page_impressions = current["page_impressions"]
                search_data.page_positions = current["page_positions"]
                search_data.page_ctr = current["page_ctr"]
        except Exception as e:
            print(f"   ! GSC search analytics failed: {e}", file=sys.stderr)

        # Fetch previous period for trend comparison
        try:
            previous = self._fetch_search_analytics(
                service, prop,
                prev_start.strftime("%Y-%m-%d"),
                prev_end.strftime("%Y-%m-%d"),
            )
            if previous and current:
                prev_imp = previous["total_impressions"]
                curr_imp = current["total_impressions"]
                if prev_imp > 0:
                    search_data.impressions_trend = curr_imp / prev_imp
                # Detect declining pages
                for url, curr_imps in current["page_impressions"].items():
                    prev_imps = previous["page_impressions"].get(url, 0)
                    if prev_imps > 10 and curr_imps < prev_imps * 0.7:
                        search_data.declining_pages.append(url)
        except Exception as e:
            print(f"   ! GSC trend comparison failed: {e}", file=sys.stderr)

        # Fetch index coverage via URL Inspection (sample-based)
        try:
            self._fetch_coverage_sample(service, prop, search_data, site_url)
        except Exception as e:
            print(f"   ! GSC coverage check failed: {e}", file=sys.stderr)

        return search_data

    def _fetch_search_analytics(self, service, prop: str,
                                 start_date: str, end_date: str) -> Optional[dict]:
        """Fetch search analytics with pagination."""
        all_rows = []
        start_row = 0

        while True:
            request = {
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": ["page"],
                "rowLimit": 25000,
                "startRow": start_row,
            }
            response = service.searchanalytics().query(
                siteUrl=prop, body=request
            ).execute()

            rows = response.get("rows", [])
            if not rows:
                break
            all_rows.extend(rows)
            if len(rows) < 25000:
                break
            start_row += len(rows)

        if not all_rows:
            return None

        total_impressions = sum(r.get("impressions", 0) for r in all_rows)
        total_clicks = sum(r.get("clicks", 0) for r in all_rows)
        total_position_weighted = sum(
            r.get("position", 0) * r.get("impressions", 0) for r in all_rows
        )
        avg_position = total_position_weighted / max(total_impressions, 1)
        avg_ctr = total_clicks / max(total_impressions, 1)

        page_impressions = {}
        page_positions = {}
        page_ctr = {}
        for row in all_rows:
            url = row["keys"][0]
            page_impressions[url] = row.get("impressions", 0)
            page_positions[url] = row.get("position", 0)
            page_ctr[url] = row.get("ctr", 0)

        return {
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "avg_position": round(avg_position, 1),
            "avg_ctr": round(avg_ctr, 4),
            "page_impressions": page_impressions,
            "page_positions": page_positions,
            "page_ctr": page_ctr,
        }

    def _fetch_coverage_sample(self, service, prop: str,
                                search_data: SearchData, site_url: str):
        """Estimate index coverage from search analytics data.

        Uses the number of pages with impressions vs total crawled pages
        as a coverage proxy. The URL Inspection API is rate-limited (2000/day)
        so we avoid it for large sites.
        """
        pages_with_impressions = len(search_data.page_impressions)
        if pages_with_impressions > 0:
            search_data.indexed_pages = pages_with_impressions
