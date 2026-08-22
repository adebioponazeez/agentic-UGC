#!/usr/bin/env python3
"""
COMPETITOR SELECTION ALGORITHM v1.0
Algorithm for selecting 20M–500M subscriber channels for reverse engineering.
High-performance tier focus: 300M–500M (GOAT-level channels with proven scale, structural validity, and institutional intelligence accumulation).
"""

from typing import Dict, List, Optional


class CompetitorSelectionAlgorithm:
    """Non-copying selection — filters competitors by structural validity, not vanity."""

    SUBSCRIBER_MIN = 20_000_000
    SUBSCRIBER_MAX = 500_000_000

    # Helper filter functions (static — avoid lambda scope issues)
    @staticmethod
    def filter_subscriber_range(s: int) -> bool:
        return 20_000_000 <= s <= 500_000_000

    @staticmethod
    def filter_vertical_alignment(aligned_dims: List[str]) -> bool:
        return len(aligned_dims) >= 2

    @staticmethod
    def filter_performance_valid(growth_rate: float, retention: float) -> bool:
        return growth_rate > 0 and retention > 0.3

    @staticmethod
    def filter_originality_verified(identity_claim: bool) -> bool:
        return bool(identity_claim)

    @staticmethod
    def filter_evidence_integrity(citations: List) -> bool:
        return bool(citations) and len(citations) > 0

    # Filter reference map
    FILTER_MAP = {
        "subscriber_range_valid": filter_subscriber_range.__func__,
        "vertical_alignment_valid": filter_vertical_alignment.__func__,
        "performance_validity": filter_performance_valid.__func__,
        "originality_verified": filter_originality_verified.__func__,
        "evidence_integrity": filter_evidence_integrity.__func__,
    }

    # 4 vertical dimensions (must align ≥ 2 with strategic thesis)
    DIMENSIONS = ["topic_domain", "audience_segment", "format_approach", "monetization_model"]

    # Selection filters
    FILTER_REQUIREMENTS = {
        "subscriber_range_valid": lambda s: SUBSCRIBER_MIN <= s <= SUBSCRIBER_MAX,
        "vertical_alignment_valid": lambda dims: len(dims) >= 2,
        "performance_valid": lambda growth_rate, retention: growth_rate > 0 and retention > 0.3,
        "originality_verified": lambda identity_claim: bool(identity_claim),
        "evidence_integrity": lambda citations: bool(citations) and len(citations) > 0,
    }

    @classmethod
    def select_competitors(cls, strategic_thesis: Dict, candidates: List[Dict]) -> List[Dict]:
        selected = []
        rejected = []

        for candidate in candidates:
            selection_report = {
                "candidate_id": candidate.get("channel_id"),
                "channel_name": candidate.get("channel_name"),
                "subscribers": candidate.get("subscribers"),
                "selection_status": "PENDING",
                "filters_passed": [],
                "filters_failed": [],
                "vertical_alignment_dimensions": [],
                "selection_reasoning": "",
                "reverse_engineering_approved": False,
            }

            # Filter 1: Subscriber range
            subscribers = candidate.get("subscribers", 0)
            filter_fn = cls.FILTER_MAP.get("subscriber_range_valid", lambda s: False)
            if filter_fn(subscribers):
                selection_report["filters_passed"].append("subscriber_range")
            else:
                selection_report["filters_failed"].append("subscriber_range")

            # Filter 2: Vertical alignment (must match ≥ 2 dimensions with thesis)
            thesis_dims = strategic_thesis.get("vertical_dimensions", [])
            candidate_dims = candidate.get("vertical_dimensions", [])
            aligned = [d for d in cls.DIMENSIONS if d in thesis_dims and d in candidate_dims]
            selection_report["vertical_alignment_dimensions"] = aligned

            filter_fn = cls.FILTER_MAP.get("vertical_alignment_valid", lambda d: False)
            if filter_fn(aligned):
                selection_report["filters_passed"].append("vertical_alignment")
            else:
                selection_report["filters_failed"].append("vertical_alignment")

            # Filter 3: Performance validity
            growth_rate = candidate.get("subscriber_growth_rate_30d", 0)
            retention_avg = candidate.get("retention_avg_30s", 0)
            filter_fn = cls.FILTER_MAP.get("performance_validity", lambda g, r: False)
            if filter_fn(growth_rate, retention_avg):
                selection_report["filters_passed"].append("performance_validity")
            else:
                selection_report["filters_failed"].append("performance_validity")

            # Filter 4: Originality (identity claim must exist and be verifiable)
            identity_claim = candidate.get("identity_claim_documented", False)
            filter_fn = cls.FILTER_MAP.get("originality_verified", lambda c: False)
            if filter_fn(identity_claim):
                selection_report["filters_passed"].append("originality_verified")
            else:
                selection_report["filters_failed"].append("originality_verified")

            # Filter 5: Evidence integrity
            citations = candidate.get("evidence_citations", [])
            filter_fn = cls.FILTER_MAP.get("evidence_integrity", lambda c: False)
            if filter_fn(citations):
                selection_report["filters_passed"].append("evidence_integrity")
            else:
                selection_report["filters_failed"].append("evidence_integrity")

            # Selection decision
            passed = len(selection_report["filters_passed"])
            required = 5  # 5 filter dimensions
            if passed == required:
                selection_report["selection_status"] = "SELECTED"
                selection_report["reverse_engineering_approved"] = True
                selection_report["selection_reasoning"] = f"All {required} filters passed. Vertical alignment: {aligned}. Ready for structural extraction (14 dimensions)."
                selected.append(selection_report)
            elif passed >= 3:
                selection_report["selection_status"] = "CONDITIONAL"
                selection_report["selection_reasoning"] = f"{passed}/{required} filters passed. Requires red team review for missing filters: {selection_report['filters_failed']}."
            else:
                selection_report["selection_status"] = "REJECTED"
                selection_report["reverse_engineering_approved"] = False
                selection_report["selection_reasoning"] = f"Only {passed}/{required} filters passed. Insufficient structural validity for reverse engineering."
                rejected.append(selection_report)

        return {
            "selection_timestamp": None,  # Would be set by caller
            "strategic_thesis_ref": strategic_thesis.get("thesis_id"),
            "algorithm_version": "v1.0.0",
            "total_candidates": len(candidates),
            "selected_for_reverse_engineering": len(selected),
            "conditional_review_required": len([r for r in selected + rejected if r["selection_status"] == "CONDITIONAL"]),
            "rejected": len(rejected),
            "selected_reports": selected,
            "rejected_reports": rejected,
            "non_copying_rule_applied": True,
        }


if __name__ == "__main__":
    algorithm = CompetitorSelectionAlgorithm()
    thesis = {
        "thesis_id": "thesis-cinema-01",
        "vertical_dimensions": ["topic_domain", "format_approach", "audience_segment"],
    }
    candidates = [
        {
            "channel_id": "comp-001",
            "channel_name": "Documentary Channel X",
            "subscribers": 150_000_000,
            "vertical_dimensions": ["topic_domain", "format_approach", "monetization_model"],
            "subscriber_growth_rate_30d": 0.08,
            "retention_avg_30s": 0.55,
            "identity_claim_documented": True,
            "evidence_citations": ["https://example.com/video/1", "https://example.com/video/2"],
        },
        {
            "channel_id": "comp-002",
            "channel_name": "Generic AI Spam Channel",
            "subscribers": 5_000_000,
            "vertical_dimensions": ["topic_domain"],
            "subscriber_growth_rate_30d": -0.05,
            "retention_avg_30s": 0.15,
            "identity_claim_documented": False,
            "evidence_citations": [],
        },
    ]
    result = algorithm.select_competitors(thesis, candidates)
    print(json.dumps(result, indent=2, default=str))
