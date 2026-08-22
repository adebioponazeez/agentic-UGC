#!/usr/bin/env python3
"""
OMEGA-Y1 SGNL FILTER ENGINE v1.0
Signal Not Generic / Noise Eliminated — executable framework.
"""

import json
from typing import Dict, List, Optional


class SignalNoiseFilterEngine:
    """SGNL framework — evaluates content proposals and competitor insights."""

    SIGNAL_DIMENSIONS = ["retention", "sentiment", "search", "propagation", "conversion"]
    NOISE_TRIGGERS = [
        "low_retention_prediction",
        "low_sentiment_prediction",
        "missing_search_signal",
        "propagation_not_approved",
        "conversion_link_invalid",
        "generic_format_unverified",
        "anti_slop_check_failed",
        "pollution_too_high",
        "red_team_unresolved",
    ]

    THRESHOLDS = {
        "retention_30s": 0.50,
        "positive_sentiment": 0.75,
        "pollution_max": 0.30,
        "signal_min_publish": 0.60,
        "signal_scale_fast": 0.80,
    }

    @classmethod
    def evaluate_proposal(cls, proposal: Dict) -> Dict:
        """Core evaluation — returns structured recommendation with evidence."""
        signal_score = 0.0
        noise_flags = []
        dimension_met = []

        # Dimension 1: Retention
        retention = proposal.get("predicted_retention_30s", 0)
        if retention >= cls.THRESHOLDS["retention_30s"]:
            signal_score += 0.20
            dimension_met.append("retention")
        else:
            noise_flags.append("low_retention_prediction")

        # Dimension 2: Sentiment
        sentiment = proposal.get("positive_sentiment_prediction", 0)
        if sentiment >= cls.THRESHOLDS["positive_sentiment"]:
            signal_score += 0.20
            dimension_met.append("sentiment")
        else:
            noise_flags.append("low_sentiment_prediction")

        # Dimension 3: Search Signal
        if proposal.get("search_signal_present", False):
            signal_score += 0.20
            dimension_met.append("search")
        else:
            noise_flags.append("missing_search_signal")

        # Dimension 4: Propagation
        if proposal.get("propagation_approved", False):
            signal_score += 0.20
            dimension_met.append("propagation")
        else:
            noise_flags.append("propagation_not_approved")

        # Dimension 5: Conversion
        if proposal.get("conversion_link_valid", False):
            signal_score += 0.20
            dimension_met.append("conversion")
        else:
            noise_flags.append("conversion_link_invalid")

        # Hard noise checks (any trigger requires action)
        if not proposal.get("originality_claim_verified", False):
            noise_flags.append("generic_format_unverified")

        if not proposal.get("anti_slop_check_passed", False):
            noise_flags.append("anti_slop_check_failed")

        pollution = proposal.get("context_pollution_score", 1.0)
        if pollution > cls.THRESHOLDS["pollution_max"]:
            noise_flags.append("pollution_too_high")

        if not proposal.get("red_team_review_complete", False):
            noise_flags.append("red_team_unresolved")

        # Recommendation logic
        if len(noise_flags) >= 2:
            recommendation = "ABANDON"
        elif len(noise_flags) == 1:
            recommendation = "REWORK"
        else:
            if signal_score >= cls.THRESHOLDS["signal_scale_fast"]:
                recommendation = "SCALE_FAST"
            elif signal_score >= cls.THRESHOLDS["signal_min_publish"]:
                recommendation = "PUBLISH"
            else:
                recommendation = "REWORK"

        return {
            "engine": "OMEGA-Y1-SGNL",
            "version": "v1.0.0",
            "signal_score": round(signal_score, 3),
            "signal_dimensions_met": dimension_met,
            "signal_dimensions_total": len(cls.SIGNAL_DIMENSIONS),
            "signal_ratio": len(dimension_met) / len(cls.SIGNAL_DIMENSIONS),
            "noise_flags": noise_flags,
            "noise_count": len(noise_flags),
            "thresholds_applied": cls.THRESHOLDS,
            "recommendation": recommendation,
            "red_team_required": recommendation in ("REWORK", "ABANDON", "SCALE_FAST"),
            "scale_authorization_required": recommendation == "SCALE_FAST",
            "proposal_ref": proposal.get("proposal_id"),
            "evaluation_timestamp": proposal.get("timestamp"),
            "execution_guidance": cls._execution_guidance(recommendation, dimension_met, noise_flags),
        }

    @classmethod
    def _execution_guidance(cls, recommendation: str, dimensions_met: List[str], noise_flags: List[str]) -> List[str]:
        guidance = []
        if recommendation == "ABANDON":
            guidance.append("Archive proposal in FAILURE MEMORY with noise reason documentation.")
            guidance.append("Generate alternative hypothesis within 48 hours.")
            guidance.append("Do not proceed to production.")
        elif recommendation == "REWORK":
            guidance.append("Address noise flags: fix generic format, verify originality claim, reduce pollution, complete red team.")
            guidance.append("Re-submit to SGNL filter after corrections.")
            guidance.append("Write rework reason to FAILURE MEMORY.")
        elif recommendation == "PUBLISH":
            guidance.append("Proceed to production with quality engine verification.")
            guidance.append("Execute red team review (critical path only).")
            guidance.append("Package with analytics hooks and memory pin configuration.")
        elif recommendation == "SCALE_FAST":
            guidance.append("MANDATORY: Full red team review (10 critics) before scale authorization.")
            guidance.append("MANDATORY: Governance Guardian approval (OMEGA-M4) before resource reallocation.")
            guidance.append("MANDATORY: Human gate confirmation for budget/channel/resource changes.")
            guidance.append("Execute scale protocol: observation → proposal → approval → integration → observation.")
        return guidance

    @classmethod
    def evaluate_competitor_insight(cls, insight: Dict) -> Dict:
        """Apply SGNL framework to reverse-engineered competitor insights."""
        proposal = {
            "proposal_id": insight.get("competitor_insight_id"),
            "predicted_retention_30s": insight.get("predicted_retention_from_transform", 0.5),
            "positive_sentiment_prediction": insight.get("predicted_sentiment_from_transform", 0.75),
            "search_signal_present": insight.get("search_relevance", False),
            "propagation_approved": insight.get("propagation_plan_approved", False),
            "conversion_link_valid": insight.get("conversion_path_valid", False),
            "originality_claim_verified": insight.get("identity_claim_verified", False),
            "anti_slop_check_passed": insight.get("anti_slop_check_passed", False),
            "context_pollution_score": insight.get("pollution_score", 0.3),
            "red_team_review_complete": insight.get("red_team_complete", False),
        }
        result = cls.evaluate_proposal(proposal)
        result["insight_ref"] = insight.get("competitor_id")
        result["insight_type"] = "reverse_engineered"
        result["transformation_verified"] = insight.get("transformation_plan_verified", False)
        return result


if __name__ == "__main__":
    engine = SignalNoiseFilterEngine()
    proposal = {
        "proposal_id": "test-01",
        "predicted_retention_30s": 0.72,
        "positive_sentiment_prediction": 0.88,
        "search_signal_present": True,
        "propagation_approved": True,
        "conversion_link_valid": True,
        "originality_claim_verified": True,
        "anti_slop_check_passed": True,
        "context_pollution_score": 0.15,
        "red_team_review_complete": False,
    }
    print(json.dumps(engine.evaluate_proposal(proposal), indent=2))
