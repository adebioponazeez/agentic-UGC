#!/usr/bin/env python3
"""
OMEGA ANALYTICS ENGINE v1.0
Every event feeds institutional memory. Every metric connects to decision.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

from core.memory.interface import MemoryBank


class AnalyticsSchema:
    """Structured event tracking with memory integration."""

    EVENT_TYPES = [
        "content_view", "content_retention", "content_click",
        "comment_post", "search_signal", "conversion", "purchase",
        "subscription", "agent_action", "memory_write",
        "state_transition", "red_team_review", "quality_score",
        "error_event", "evolution_proposal"
    ]

    def __init__(self, memory_bank: Optional[MemoryBank] = None):
        self.memory = memory_bank or MemoryBank()
        self.event_log: List[Dict] = []

    def record_event(
        self,
        event_type: str,
        agent_id: Optional[str] = None,
        task_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        content_id: Optional[str] = None,
        dimensions: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, float]] = None,
        quality_indicators: Optional[Dict[str, float]] = None,
        memory_updates: Optional[List[str]] = None,
        context_packet_ref: Optional[str] = None,
    ) -> Dict:
        if event_type not in self.EVENT_TYPES:
            # Still record but log warning
            pass

        event = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_id": agent_id,
            "task_id": task_id,
            "channel_id": channel_id,
            "content_id": content_id,
            "dimensions": dimensions or {},
            "metrics": metrics or {},
            "memory_updates": memory_updates or [],
            "quality_indicators": quality_indicators or {},
            "context_packet_ref": context_packet_ref,
        }
        self.event_log.append(event)

        # Write to audience memory if relevant
        if event_type in ["content_view", "content_retention", "content_click", "conversion", "purchase", "subscription"]:
            self.memory.write_memory(
                bank_id="AUDIENCE",
                content={
                    "event_ref": event["event_id"],
                    "event_type": event_type,
                    "channel_id": channel_id,
                    "content_id": content_id,
                    "metrics": event["metrics"],
                    "dimensions": event["dimensions"],
                },
                agent_id=agent_id,
                task_id=task_id,
                tags=[f"analytics:{event_type}"],
            )

        # Write to operational memory for agent/state events
        if event_type in ["agent_action", "memory_write", "state_transition", "red_team_review", "evolution_proposal"]:
            self.memory.write_memory(
                bank_id="OPERATIONAL",
                content=event,
                agent_id=agent_id,
                task_id=task_id,
                tags=["analytics", event_type],
            )

        # Write to failure memory for errors
        if event_type == "error_event":
            self.memory.write_memory(
                bank_id="FAILURE",
                content={
                    "error_event_ref": event["event_id"],
                    "description": event.get("dimensions", {}).get("error_message", "Unknown error"),
                    "agent_id": agent_id,
                    "task_id": task_id,
                    "new_guardrail_proposed": False,
                },
                agent_id=agent_id,
                task_id=task_id,
                tags=["analytics_error"],
            )

        return event

    def get_quality_indicators_for_output(self, output_ref: str) -> Dict[str, float]:
        # Would aggregate from red team reviews and analytics
        # For v1.0: return simulated/placeholder with structure
        return {
            "omega_score": 0.72,
            "truth_score": 0.85,
            "production_score": 0.88,
            "business_score": 0.65,
            "risk_score": 0.15,
            "calculation": "C × T × P × B × (1 - R) = 0.72",
            "reference_output": output_ref,
        }

    def build_dashboard_config(self) -> Dict:
        return {
            "dashboard_title": "OMEGA MEDIA OS v1.0 — Analytics",
            "panels": [
                {"title": "System Health", "metrics": ["agent_activation_time", "context_pollution_score", "memory_sync_time"], "role": "all"},
                {"title": "Content Performance", "metrics": ["retention_30s", "watch_time", "positive_sentiment"], "role": "creator"},
                {"title": "Product Pipeline", "metrics": ["mvp_visits", "conversion_rate", "presell_signups"], "role": "entrepreneur"},
                {"title": "Cinema Quality", "metrics": ["visual_quality_score", "cinematic_identity_score", "truth_accuracy"], "role": "filmmaker"},
                {"title": "Portfolio Intelligence", "metrics": ["channel_experiment_status", "memory_growth", "learning_velocity"], "role": "architect"},
                {"title": "Governance & Security", "metrics": ["governance_violations", "red_team_completion_rate", "self_modification_attempts"], "role": "sovereign"},
            ],
            "alert_rules_ref": "analytics/SCHEMA.md",
        }


if __name__ == "__main__":
    analytics = AnalyticsSchema()
    event = analytics.record_event(
        event_type="content_view",
        agent_id="OMEGA-C2",
        task_id="task-42",
        channel_id="OMEGA-DOCUMENTARY",
        content_id="content-42",
        metrics={"retention_30s": 0.62, "watch_time_total": 240},
        dimensions={"device": "mobile", "region": "NA"},
        quality_indicators={"omega_score": 0.72},
    )
    print(json.dumps(event, indent=2, default=str))
