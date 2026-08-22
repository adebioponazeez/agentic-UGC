#!/usr/bin/env python3
"""
MEMORY INTEGRATION — REVERSE ENGINEERING v1.0
How competitor insights feed institutional memory without duplication.
"""

import json
from typing import Dict, Optional

try:
    from core.memory.interface import MemoryBank
except ImportError:
    MemoryBank = None


class ReverseEngineeringMemoryIntegration:
    """Integrates validated/rejected competitor patterns into 6 memory banks."""

    BANKS = ["WORLD", "STRATEGIC", "CREATIVE", "OPERATIONAL", "AUDIENCE", "FAILURE"]

    def __init__(self, memory_bank: Optional[Any] = None):
        self.memory = memory_bank or (MemoryBank() if MemoryBank else None)

    def integrate_insight(self, insight_report: Dict, transformation_plan: Dict, anti_cloning_result: Dict) -> Dict:
        memory_updates = []

        # If approved (all anti-cloning checks passed) → write validated patterns
        if anti_cloning_result.get("all_checks_passed", False):
            # Creative Memory: validated format/pattern observations
            if insight_report.get("dimensions", {}):
                creative_result = self.memory.write_memory(
                    bank_id="CREATIVE",
                    content={
                        "insight_ref": insight_report.get("competitor_id"),
                        "pattern_type": "validated_from_reverse_engineering",
                        "dimensions_analyzed": list(insight_report.get("dimensions", {}).keys()),
                        "transformation_plan_ref": transformation_plan.get("plan_id"),
                        "red_team_review_required": transformation_plan.get("red_team_required", True),
                        "identity_claim": transformation_plan.get("identity_claim_verified"),
                    },
                    agent_id="OMEGA-Y1",
                    tags=["reverse_engineering", "validated", "transformation_applied"],
                    confidence=0.85 if insight_report.get("evidence_integrity_score", 0) > 0.7 else 0.65,
                )
                memory_updates.append({"bank": "CREATIVE", "entry_id": creative_result.get("entry_id"), "status": "VALIDATED"})

            # Strategic Memory: competitive landscape + strategic thesis adjustments
            strategic_result = self.memory.write_memory(
                bank_id="STRATEGIC",
                content={
                    "competitive_insight_id": insight_report.get("competitor_id"),
                    "vertical_dimensions_aligned": insight_report.get("vertical_alignment_dimensions", []),
                    "transformation_strategy": transformation_plan.get("strategy_ref"),
                    "scale_recommendation": transformation_plan.get("scale_recommendation"),
                    "approval_reference": anti_cloning_result.get("aggregate_status"),
                },
                agent_id="OMEGA-Y1",
                tags=["competitive_intelligence", "strategic"],
            )
            memory_updates.append({"bank": "STRATEGIC", "entry_id": strategic_result.get("entry_id"), "status": "VALIDATED"})

        # If rejected → write failure/rejected pattern
        if not anti_cloning_result.get("all_checks_passed", False):
            failure_result = self.memory.write_memory(
                bank_id="FAILURE",
                content={
                    "failure_type": "reverse_engineering_rejected",
                    "reason": "Anti-cloning checks failed: " + ", ".join(
                        k for k, v in anti_cloning_result.get("results", {}).items()
                        if v.get("status") == "FAIL"
                    ),
                    "competitor_ref": insight_report.get("competitor_id"),
                    "new_guardrail": "Every reverse-engineered insight requires transformation plan + identity claim + anti-cloning verification before memory integration.",
                    "fix_action": "Redesign transformation plan; verify identity claim; resubmit to anti-cloning guardian.",
                    "test_result": "Anti-cloning checks not passed.",
                },
                agent_id="OMEGA-M4",
                tags=["reverse_engineering", "rejected", "anti_cloning"],
                deletion_policy="permanent",
            )
            memory_updates.append({"bank": "FAILURE", "entry_id": failure_result.get("entry_id"), "status": "REJECTED"})

        # Operational Memory: always write — audit trail
        operational_result = self.memory.write_memory(
            bank_id="OPERATIONAL",
            content={
                "integration_event": "reverse_engineering_memory_sync",
                "competitor_id": insight_report.get("competitor_id"),
                "anti_cloning_aggregate": anti_cloning_result.get("aggregate_status"),
                "checks_passed": anti_cloning_result.get("all_checks_passed"),
                "transformation_plan_ref": transformation_plan.get("plan_id"),
                "memory_updates": memory_updates,
                "rollback_reference": transformation_plan.get("rollback_ref"),
            },
            agent_id="OMEGA-Y1",
            tags=["memory_integration", "reverse_engineering"],
        )
        memory_updates.append({"bank": "OPERATIONAL", "entry_id": operational_result.get("entry_id"), "status": "AUDIT"})

        return {
            "integration_agent": "OMEGA-Y1 + M4",
            "memory_updates_executed": memory_updates,
            "integration_approved": anti_cloning_result.get("all_checks_passed", False),
            "audit_reference": operational_result.get("entry_id"),
        }
