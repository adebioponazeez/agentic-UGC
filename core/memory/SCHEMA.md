# OMEGA MEMORY ARCHITECTURE v1.0
## Six Institutional Memory Banks + Context Packet Engine

---

## 1. SCHEMA OVERVIEW

Every memory entry is a structured object with mandatory fields:

```json
{
  "entry_id": "uuid-v4",
  "bank_id": "WORLD | STRATEGIC | CREATIVE | OPERATIONAL | AUDIENCE | FAILURE",
  "timestamp": "ISO8601",
  "agent_id": "string",
  "task_id": "uuid",
  "content": "string or structured object",
  "vector_embedding": "array[float] (optional, computed on write)",
  "graph_edges": [
    {"target_entry_id": "...", "relation_type": "..."}
  ],
  "confidence": 0.0,
  "access_level": "public | internal | restricted | governance",
  "deletion_policy": "permanent | review_after:days | temporary",
  "tags": ["string"]
}
```

---

## 2. BANK SPECIFICATIONS

### 2.1 WORLD MEMORY (WORLD)
**What exists?** Entities, facts, signals, competitors, external events.

```json
{
  "bank_id": "WORLD",
  "entry_types": [
    "entity", "signal", "event", "competitor_action", "trend", "fact_check"
  ],
  "required_sources": ["memory_ref", "web_evidence_url", "agent_observation"],
  "update_frequency": "continuous",
  "deletion_policy": "permanent (facts); review_after_30 (signals); temporary (trends)"
}
```

**Key Queries:**
- Find entities related to current problem (vector similarity + graph traversal)
- Find recent competitor actions (timestamp filter)
- Find validated facts that contradict current hypothesis (graph contradiction search)

---

### 2.2 STRATEGIC MEMORY (STRATEGIC)
**Why are we doing it?** Thesis, objectives, tradeoffs, strategic shifts, resource allocation.

```json
{
  "bank_id": "STRATEGIC",
  "entry_types": ["thesis_statement", "objective", "tradeoff", "decision_record",
                   "resource_allocation", "strategic_shift"],
  "required_sources": ["human_approval_ref", "agent_analysis", "red_team_review"],
  "update_frequency": "per decision (manual gate); weekly review",
  "deletion_policy": "permanent (decisions); review_after_90 (objectives)"
}
```

**Governance Rule:** Strategic memory can only be modified with `Governance Guardian` approval and `Self-Evolution Engine` proposal reference.

---

### 2.3 CREATIVE MEMORY (CREATIVE)
**What creative patterns work?** Hooks, formats, emotional arcs, visual patterns, narrative structures, audience responses to specific patterns.

```json
{
  "bank_id": "CREATIVE",
  "entry_types": ["hook_pattern", "format_template", "emotional_arc", "visual_grammar",
                   "narrative_structure", "audience_response_pattern", "format_experiment"],
  "required_sources": ["content_output_ref", "analytics_event_ref", "red_team_review_ref"],
  "update_frequency": "per content output + per analytics event",
  "deletion_policy": "permanent (validated patterns); temporary (failed experiments)"
}
```

**Compounding Mechanism:** Every validated pattern creates a graph edge to the format/template it improves. Over time, the graph becomes institutional creative intelligence.

---

### 2.4 OPERATIONAL MEMORY (OPERATIONAL)
**How do we execute?** Workflows, templates, configurations, agent registry changes, deployment logs, automation rules.

```json
{
  "bank_id": "OPERATIONAL",
  "entry_types": ["workflow_template", "agent_config", "deployment_log",
                   "automation_rule", "tool_interface_version", "context_packet_example"],
  "required_sources": ["agent_id", "version_ref", "test_result_ref"],
  "update_frequency": "per deployment; per agent update",
  "deletion_policy": "permanent (deployed versions); temporary (draft templates)"
}
```

---

### 2.5 AUDIENCE MEMORY (AUDIENCE)
**What does audience do?** Behavior patterns, retention curves, comment clusters, search signals, conversion paths, segment definitions.

```json
{
  "bank_id": "AUDIENCE",
  "entry_types": ["behavior_pattern", "retention_curve", "comment_cluster",
                   "search_signal", "conversion_path", "segment_profile",
                   "feedback_summary"],
  "required_sources": ["analytics_event_ref", "interview_ref", "survey_result_ref"],
  "update_frequency": "continuous (analytics); weekly (interview synthesis)",
  "deletion_policy": "permanent (behavior patterns); temporary (daily signals)"
}
```

**Privacy / Policy Note:** Audience memory must not contain personally identifiable information. Only aggregate patterns and anonymized signals.

---

### 2.6 FAILURE MEMORY (FAILURE)
**What must not recur?** Errors, root causes, fixes, tests, new guardrails. Non-deletable.

```json
{
  "bank_id": "FAILURE",
  "entry_types": ["failure_event", "root_cause", "fix_action", "test_result",
                   "new_guardrail", "rollback_reference"],
  "required_sources": ["error_log_ref", "agent_id", "red_team_review_ref", "fix_verification_ref"],
  "update_frequency": "on every failure (immediate); on every fix (verified); weekly audit",
  "deletion_policy": "permanent (never delete)"
}
```

**Structure (Mandatory):**
Every entry must include:
1. `Failure`: What happened?
2. `Cause`: Root cause (not symptom)
3. `Fix`: What was changed?
4. `Test`: How was the fix verified?
5. `New Guardrail`: What prevents recurrence?

---

## 3. CONTEXT PACKET ENGINE (ANTI-POLLUTION)

Every agent interaction uses a structured context packet. Maximum size: **10KB uncompressed**.

```json
{
  "packet_id": "uuid",
  "version": "1.0",
  "timestamp": "ISO8601",
  "agent_context": {
    "agent_id": "string",
    "role": "string",
    "task_id": "uuid"
  },
  "runtime_context": {
    "current_state": "string (state machine phase)",
    "previous_action": "string",
    "errors": ["string"],
    "tool_results": {"tool_id": "result_summary"},
    "dependencies": ["task_id"],
    "next_action_target": "string"
  },
  "memory_pins": [
    {"bank_id": "WORLD", "entry_id": "...", "relevance_score": 0.95},
    {"bank_id": "FAILURE", "entry_id": "...", "relevance_score": 0.87},
    {"bank_id": "STRATEGIC", "entry_id": "...", "relevance_score": 0.82}
  ],
  "project_context": {
    "project_id": "string",
    "thesis_statement": "string (≤ 200 chars)",
    "format_constraints": ["string"],
    "story_rules": "string",
    "research_evidence": "string",
    "assets_available": ["file_path"],
    "deadlines": {"deliverable": "ISO8601"},
    "quality_bar": {"min_omega_score": 0.6}
  },
  "agent_contract": {
    "role": "string",
    "task": "string",
    "available_tools": ["tool_ref"],
    "relevant_knowledge": ["bank:entry_id"],
    "output_contract_ref": "docs/contracts/OUTPUT_CONTRACT.md",
    "failure_conditions_ref": "core/agent_registry.yaml"
  },
  "state_transition": {
    "current_phase": "string",
    "target_phase": "string",
    "conditions_met": ["boolean"],
    "human_gate_required": false,
    "red_team_review_pending": false
  },
  "anti_drift_checks": {
    "max_token_estimate": 10240,
    "context_pollution_score": 0.0,
    "last_memory_sync": "ISO8601"
  }
}
```

**Anti-Pollution Rules:**
- If `context_pollution_score` > 0.3, agent must request packet refresh.
- Memory pins must not exceed 10 entries.
- `project_context` must reference `thesis_statement` (prevents strategic drift).
- Every packet must include at least one `FAILURE` memory pin (prevents repeated errors).

---

## 4. VECTOR + GRAPH + EPISODIC STORAGE

```
VECTOR (Semantic Search):
- Model: text-embedding-3-large or equivalent
- Storage: pgvector / Weaviate / Chroma
- Query: cosine similarity with bank filter

GRAPH (Relationship):
- Nodes: memory entries
- Edges: explicit references + inferred similarity + temporal sequence
- Query: shortest path, common neighbors, contradiction detection

EPISODIC (Sequence):
- Ordered events per project/task
- Enables replay, rollback, and temporal reasoning
- Storage: PostgreSQL with temporal indexing
```

Every agent must declare which memory modes it uses in its `RELEVANT_KNOWLEDGE` field.

---

## 5. MEMORY ACCESS PROTOCOL

```python
def read_memory(bank_id, query, mode="vector", max_results=5, min_confidence=0.7):
    # Vector search across embeddings
    # Graph traversal from query node
    # Episodic retrieval by task / agent / timestamp
    # Filter by access_level
    # Return structured results with relevance scores

    pass

def write_memory(bank_id, entry, mode="persistent"):
    # Validate schema
    # Compute embedding
    # Create graph edges
    # Check against FAILURE memory for contradictions
    # Log in OPERATIONAL memory
    # Return entry_id and rollback reference
    pass
```

---

## 6. MEMORY INTEGRATION WITH WORKFLOWS

Every workflow phase requires specific memory operations:

```
OBSERVE     → Read WORLD + AUDIENCE (current signals)
CAPTURE     → Write WORLD (new signal) + OPERATIONAL (capture log)
CLASSIFY    → Read STRATEGIC (thesis alignment) + CREATIVE (pattern match)
CONNECT     → Read + Write GRAPH edges across banks
RESEARCH    → Read WORLD + STRATEGIC + FAILURE (similar past failures)
SYNTHESIZE  → Read CREATIVE + STRATEGIC; Write STRATEGIC (new insight)
HYPOTHESIZE → Read STRATEGIC; Write OPERATIONAL (proposal log)
CHALLENGE   → Read FAILURE (counter-evidence); Write OPERATIONAL (challenge log)
PRIORITIZE  → Read STRATEGIC + WORLD + OPERATIONAL
DESIGN      → Read CREATIVE + WORLD; Write OPERATIONAL (design doc)
SIMULATE    → Read OPERATIONAL (simulation config); Write OPERATIONAL (sim result)
PRODUCE     → Read OPERATIONAL (workflow); Write WORLD (output fact) + CREATIVE (pattern validation)
VERIFY      → Read FAILURE (guardrails); Write OPERATIONAL (verification log)
PACKAGE     → Read OPERATIONAL (packaging spec)
DISTRIBUTE  → Read OPERATIONAL + AUDIENCE (channel state)
MEASURE     → Write AUDIENCE (behavior); Read WORLD (external response)
DIAGNOSE    → Read ALL BANKS (holistic); Write STRATEGIC (diagnosis) + FAILURE (if error)
LEARN       → Read ALL; Write CREATIVE + STRATEGIC + FAILURE (if new failure)
STORE       → Write to persistent storage; update graph; sync vector index
REINVEST    → Read STRATEGIC + OPERATIONAL; update resource allocation
RECONFIGURE → Read STRATEGIC + OPERATIONAL; propose structural change
SCALE       → Read AUDIENCE + WORLD; trigger propagation through graph
```

---

## 7. FAILURE-TO-INFRASTRUCTURE LOOP

```
FAILURE EVENT (detected by agent or user or red team)
  ↓
WRITE FAILURE MEMORY (immediate)
  ↓
ROOT CAUSE ANALYSIS (agent D2 + D3 + red team)
  ↓
FIX IMPLEMENTED (agent M1 proposed, M4 approved, engineer executed)
  ↓
TEST EXECUTED (agent M3 + deployment engine)
  ↓
NEW GUARDRAIL ADDED (written to FAILURE memory + OPERATIONAL memory)
  ↓
AGENT REGISTRY UPDATED (if agent contract changed)
  ↓
MEMORY GRAPH UPDATED (new edges from failure to fix to guardrail)
  ↓
OBSERVE NEXT EXECUTION (verify guardrail prevents recurrence)
```

If recurrence happens within 30 days, escalate to governance review.
