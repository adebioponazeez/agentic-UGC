# OMEGA ANALYTICS SCHEMA v1.0
## Every event feeds institutional memory

---

## 1. EVENT TYPES (Structured Schema)

Every event is a JSON object with mandatory fields:

```json
{
  "event_id": "uuid",
  "event_type": "content_view | content_retention | content_click | comment_post | search_signal | conversion | purchase | subscription | agent_action | memory_write | state_transition | red_team_review | quality_score | error_event",
  "timestamp": "ISO8601",
  "agent_id": "string (if agent-triggered)",
  "task_id": "string (if part of workflow)",
  "channel_id": "string",
  "content_id": "string",
  "user_segment": "string (anonymized)",
  "dimensions": {"key": "value"},
  "metrics": {"key": "number"},
  "memory_updates": ["bank_id:entry_id"],
  "quality_indicators": {
    "omega_score": 0.85,
    "truth_score": 0.92,
    "production_score": 0.88,
    "business_score": 0.75,
    "risk_score": 0.12
  },
  "context_packet_ref": "string"
}
```

---

## 2. CORE METRIC CATEGORIES

### 2.1 CONTENT METRICS
```
views                        → Count
retention_curve              → Array of retention % at 10s intervals
watch_time_total             → Seconds
watch_time_average           → Seconds
click_through_rate           → Ratio
engagement_rate              → (likes + comments + shares) / views
positive_sentiment_rate      → NLP-derived ratio
search_signal_strength       → Search volume increase after publication
comment_quality_score        → Structured analysis of comment content
conversion_to_subscriber     → Ratio
conversion_to_customer       → Ratio
```

### 2.2 PRODUCT METRICS
```
mvp_visits                  → Count
presell_signups              → Count
conversion_rate              → (purchase / visit)
customer_lifetime_value_estimate → Estimated
retention_rate_30d          → Ratio
feedback_score               → Structured score from interviews / surveys
feature_usage                → Per-feature adoption
error_rate                   → Technical errors / user-reported issues
```

### 2.3 CINEMA METRICS
```
visual_quality_score         → Red team score (C component)
cinematic_identity_score     → Red team score (authorship / identity)
production_feasibility        → Production score (P component)
emotional_progression_score  → Audience retention at emotional peaks
truth_accuracy_score         → Fact-check score (T component)
```

### 2.4 AGENT / SYSTEM METRICS
```
agent_activation_time         → Seconds (execution speed target: < 10s)
context_packet_size          → Bytes (max: 10,240)
context_pollution_score      → Float [0, 1] (must be ≤ 0.3)
state_transition_accuracy    → Ratio of valid transitions
memory_sync_time             → Seconds
red_team_review_duration     → Seconds (target: < 1h)
evolution_proposal_time      → Seconds (target: < 4h from insight)
```

---

## 3. ANALYTICS EVENT FLOW

```
EVENT OCCURS (user action, agent action, system event)
  ↓
EVENT VALIDATED (schema check, identity verification)
  ↓
EVENT ENRICHED (dimensions computed, quality indicators calculated)
  ↓
MEMORY UPDATE (relevant banks updated with event reference)
  ↓
DASHBOARD UPDATE (metrics aggregated, alerts evaluated)
  ↓
INSIGHT GENERATION (if event pattern exceeds threshold, trigger analysis)
  ↓
MEMORY UPDATE (strategic / creative / audience / failure as appropriate)
```

---

## 4. ALERT RULES

```yaml
alerts:
  - name: "low_retention_alert"
    condition: "content.retention_30s < 0.30"
    severity: "high"
    action: "trigger_red_team_review; write_failure_memory; propose_rework"

  - name: "high_pollution_alert"
    condition: "agent.context_pollution_score > 0.30"
    severity: "critical"
    action: "stop_agent; refresh_context_packet; log_error; update_guardrail"

  - name: "quality_below_threshold"
    condition: "content.omega_score < 0.60"
    severity: "high"
    action: "block_publication; trigger_red_team; write_failure_memory"

  - name: "memory_sync_failure"
    condition: "system.memory_sync_time > 300"
    severity: "medium"
    action: "log_warning; retry_sync; alert_admin"

  - name: "governance_violation"
    condition: "system.governance_violation_detected == true"
    severity: "critical"
    action: "immediate_stop; log_violations; notify_human_gate"
```

---

## 5. DASHBOARD STRUCTURE

Every user role sees a tailored dashboard:

**Entrepreneur:** Revenue, conversion, customer acquisition cost, lifetime value, product pipeline
**Creator:** Content retention, audience growth, creative pattern validation, series performance
**Filmmaker:** Cinematic quality scores, production metrics, visual identity consistency, emotional progression
**Ecosystem Architect:** Channel portfolio performance, graph propagation effectiveness, memory growth, system health
**Sovereign Architect:** Strategic thesis alignment, institutional memory growth, governance integrity, evolution speed
**Forward Deployed Engineer:** Deployment status, error rates, performance metrics, test results
**Deploy Engineer:** System health, security, rollback status, monitoring coverage

---

## 6. DATA RETENTION AND PRIVACY

- Audience data: Aggregate patterns only; no PII retained in analytics schema
- Memory banks: All entries anonymized (agent IDs, not user IDs)
- Event logs: Retained for 90 days in hot storage, 1 year in cold storage, then aggregated
- Failure memory: Permanent (required by architecture)
- Rollback capability: Full event history preserved for 30 days
