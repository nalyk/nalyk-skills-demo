"""Google PageSpeed Insights API v5 client for real CWV measurement.

Free tier: 25,000 queries/day with API key, 2/min without.
"""

import json
import os
from typing import Optional

import requests

from engine import CWVData


PSI_API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


class PageSpeedClient:
    """Google PageSpeed Insights API v5 client."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("PAGESPEED_API_KEY")

    def analyze(self, url: str, strategy: str = "mobile") -> CWVData:
        """
        Get real Core Web Vitals data from PageSpeed Insights.

        Args:
            url: URL to analyze
            strategy: 'mobile' or 'desktop'

        Returns:
            CWVData with field data (CrUX) and/or lab data (Lighthouse)
        """
        params = {
            "url": url,
            "strategy": strategy,
            "category": ["performance", "accessibility", "seo", "best-practices"],
        }
        if self.api_key:
            params["key"] = self.api_key

        try:
            resp = requests.get(PSI_API_URL, params=params, timeout=60)
            if resp.status_code != 200:
                return CWVData(source="error")
            data = resp.json()
        except Exception:
            return CWVData(source="error")

        cwv = CWVData()

        # Field data (CrUX — real user measurements)
        crux = data.get("loadingExperience", {}).get("metrics", {})
        if crux:
            cwv.source = "field"

            lcp = crux.get("LARGEST_CONTENTFUL_PAINT_MS", {})
            if lcp:
                cwv.lcp_ms = lcp.get("percentile")
                cwv.lcp_rating = lcp.get("category", "unknown").lower().replace("_", "-")

            inp = crux.get("INTERACTION_TO_NEXT_PAINT", {})
            if inp:
                cwv.inp_ms = inp.get("percentile")
                cwv.inp_rating = inp.get("category", "unknown").lower().replace("_", "-")

            cls_data = crux.get("CUMULATIVE_LAYOUT_SHIFT_SCORE", {})
            if cls_data:
                percentile = cls_data.get("percentile")
                if percentile is not None:
                    cwv.cls = percentile / 100.0  # CrUX returns CLS × 100
                cwv.cls_rating = cls_data.get("category", "unknown").lower().replace("_", "-")

        # Lab data (Lighthouse)
        lighthouse = data.get("lighthouseResult", {})
        if lighthouse:
            if cwv.source == "none":
                cwv.source = "lab"

            categories = lighthouse.get("categories", {})
            perf = categories.get("performance", {})
            cwv.lighthouse_performance = int((perf.get("score") or 0) * 100)

            acc = categories.get("accessibility", {})
            cwv.lighthouse_accessibility = int((acc.get("score") or 0) * 100)

            seo = categories.get("seo", {})
            cwv.lighthouse_seo = int((seo.get("score") or 0) * 100)

            bp = categories.get("best-practices", {})
            cwv.lighthouse_best_practices = int((bp.get("score") or 0) * 100)

            # Lab-only CWV if no field data
            audits = lighthouse.get("audits", {})
            if cwv.lcp_ms is None:
                lcp_audit = audits.get("largest-contentful-paint", {})
                if lcp_audit.get("numericValue"):
                    cwv.lcp_ms = lcp_audit["numericValue"]
                    cwv.lcp_rating = self._rate_lcp(cwv.lcp_ms)

            if cwv.cls is None:
                cls_audit = audits.get("cumulative-layout-shift", {})
                if cls_audit.get("numericValue") is not None:
                    cwv.cls = cls_audit["numericValue"]
                    cwv.cls_rating = self._rate_cls(cwv.cls)

            # Opportunities
            for audit_id, audit in audits.items():
                if audit.get("details", {}).get("type") == "opportunity":
                    savings = audit.get("details", {}).get("overallSavingsMs", 0)
                    if savings > 0:
                        cwv.opportunities.append({
                            "id": audit_id,
                            "title": audit.get("title", ""),
                            "savings_ms": savings,
                            "description": audit.get("description", "")[:200],
                        })

            cwv.opportunities.sort(key=lambda x: x.get("savings_ms", 0), reverse=True)

        return cwv

    @staticmethod
    def _rate_lcp(ms: float) -> str:
        if ms < 2500:
            return "good"
        elif ms < 4000:
            return "needs-improvement"
        return "poor"

    @staticmethod
    def _rate_cls(score: float) -> str:
        if score < 0.1:
            return "good"
        elif score < 0.25:
            return "needs-improvement"
        return "poor"
