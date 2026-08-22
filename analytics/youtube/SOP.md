# ANALYTICS SCHEMA — YOUTUBE OPERATIONS v1.0
## Structured event types for content, competitor intelligence, scale, and failure tracking

---

## EVENT TYPE EXTENSIONS (to `analytics/SCHEMA.md`)

```json
{
  "youtube_video_published": {
    "description": "Content published through 60-channel topology with SGNL verification",
    "required_dimensions": ["channel_id", "content_id", "series_id", "format_type", "editorial_constitution_version"],
    "required_metrics": ["duration_seconds", "retention_predicted_30s", "quality_omega_score", "signal_noise_filter_recommendation"],
    "memory_updates": ["CREATIVE", "OPERATIONAL", "AUDIENCE"],
    "red_team_required": true,
    "quality_engine_applied": true,
  },
  "youtube_retention_curve": {
    "description": "Audience retention measurement — feeds Creative + Audience Memory",
    "required_dimensions": ["video_id", "segment", "device_type", "region"],
    "required_metrics": ["retention_10s", "retention_30s", "retention_60s", "retention_full", "watch_time_total"],
    "memory_updates": ["AUDIENCE", "CREATIVE"],
    "threshold_alert": "retention_30s < 0.30 triggers red_team_review; retention_30s < 0.15 triggers abandon_protocol",
  },
  "youtube_search_signal": {
    "description": "Search volume and query behavior — feeds World + Audience Memory",
    "required_dimensions": ["topic_cluster", "search_volume_change_7d", "related_queries", "search_intent"],
    "required_metrics": ["search_volume_absolute", "search_volume_growth_rate", "search_signal_strength_score"],
    "memory_updates": ["WORLD", "AUDIENCE", "STRATEGIC"],
    "scale_trigger": "search_signal_strength_score > 0.2 and retention_30s > 0.6 for 3+ videos in series",
  },
  "youtube_competitor_insight": {
    "description": "Reverse-engineered competitor structure — feeds Creative + Strategic Memory",
    "required_dimensions": ["competitor_channel_id", "vertical_dimensions_aligned", "evidence_references", "transformation_plan_ref"],
    "required_metrics": ["subscribers", "retention_avg_30s", "growth_rate_30d", "evidence_integrity_score"],
    "memory_updates": ["CREATIVE", "STRATEGIC"],
    "red_team_required": true,
    "anti_cloning_verification": true,
  },
  "youtube_scale_trigger": {
    "description": "Automatic scale analysis — requires governance gate before resource reallocation",
    "required_dimensions": ["trigger_category", "evidence_reference", "current_portfolio_allocation", "proposed_allocation_change"],
    "required_metrics": ["subscriber_velocity_change", "retention_trend_change", "conversion_trend_change", "memory_growth_rate"],
    "memory_updates": ["STRATEGIC", "OPERATIONAL"],
    "governance_gate_required": true,
    "human_approval_required": true,
    "red_team_review_required": true,
  },
  "youtube_abandon_event": {
    "description": "Content or experiment abandoned — feeds Failure Memory with structured entry",
    "required_dimensions": ["experiment_id", "abandon_reason", "noise_flags_triggered", "red_team_recommendation"],
    "required_metrics": ["signal_score_at_abandon", "retention_final", "cost_invested", "learning_extracted"],
    "memory_updates": ["FAILURE", "CREATIVE"],
    "permanent_memory_write": true,
    "new_guardrail_proposed": true,
  },
  "youtube_evolution_proposal": {
    "description": "Self-evolution proposal from YouTube Operations — feeds Strategic + Operational Memory",
    "required_dimensions": ["proposal_id", "problem_statement", "evidence_reference", "test_plan_ref", "rollback_ref", "approval_status"],
    "required_metrics": ["expected_impact_metric", "confidence_interval", "resource_change_estimate"],
    "memory_updates": ["STRATEGIC", "OPERATIONAL", "FAILURE"],
    "governance_approval_required": true,
    "stress_test_scheduled": true,
  },
}
```

---

## ALERT RULES (YOUTUBE-SPECIFIC ADDITIONS)

```yaml
alerts:
  - name: "youtube_sgnl_abandon"
    condition: "youtube_abandon_event.recommendation == 'ABANDON'"
    severity: "high"
    action: "stop_production; write_failure_memory; trigger_rework_protocol; notify_red_team"

  - name: "youtube_scale_trigger_detected"
    condition: "youtube_scale_trigger.trigger_category == 'subscriber_velocity' OR 'retention_trend' OR 'conversion_trend'"
    severity: "medium"
    action: "write_strategic_memory; generate_evolution_proposal; schedule_red_team_review; block_automatic_resource_reallocation"

  - name: "youtube_competitor_insight_rejected"
    condition: "youtube_competitor_insight.anti_cloning_aggregate == 'REJECTED'"
    severity: "medium"
    action: "write_failure_memory_with_reason; archive_rejected_pattern; propose_new_experiment_with_identity_claim"

  - name: "youtube_retention_collapse"
    condition: "youtube_retention_curve.retention_30s < 0.30"
    severity: "critical"
    action: "trigger_red_team_review; write_failure_memory; evaluate_abandon_or_rework_based_on_signal_score"

  - name: "youtube_quality_below_threshold"
    condition: "youtube_video_published.quality_omega_score < 0.60"
    severity: "high"
    action: "block_distribution; trigger_full_red_team_review; require_quality_engine_reverification"

  - name: "youtube_memory_sync_failure"
    condition: "analytics_memory_sync_time > 300"
    severity: "medium"
    action: "log_warning; retry_sync; alert_admin"
```
