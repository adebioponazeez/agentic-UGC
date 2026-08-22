# CONTEXT PACKET SCHEMA v1.0
## Structured payload for agent interactions — Max 10KB uncompressed

---

## 1. SCHEMA DEFINITION (JSON Schema Draft 7)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "OMEGA_ContextPacket",
  "type": "object",
  "required": [
    "packet_id", "version", "timestamp",
    "agent_context", "runtime_context", "project_context",
    "agent_contract", "memory_pins", "state_transition",
    "anti_drift_checks"
  ],
  "properties": {
    "packet_id": {"type": "string", "format": "uuid"},
    "version": {"type": "string", "enum": ["1.0"]},
    "timestamp": {"type": "string", "format": "date-time"},
    "agent_context": {
      "type": "object",
      "required": ["agent_id", "role", "task_id"],
      "properties": {
        "agent_id": {"type": "string"},
        "role": {"type": "string"},
        "task_id": {"type": "string", "format": "uuid"}
      }
    },
    "runtime_context": {
      "type": "object",
      "required": ["current_state", "previous_action", "dependencies", "next_action_target"],
      "properties": {
        "current_state": {"type": "string"},
        "previous_action": {"type": "string"},
        "errors": {"type": "array", "items": {"type": "string"}},
        "tool_results": {"type": "object"},
        "dependencies": {"type": "array", "items": {"type": "string"}},
        "next_action_target": {"type": "string"}
      }
    },
    "memory_pins": {
      "type": "array",
      "minItems": 1,
      "maxItems": 10,
      "items": {
        "type": "object",
        "required": ["bank_id", "entry_id", "relevance_score"],
        "properties": {
          "bank_id": {"type": "string", "enum": ["WORLD", "STRATEGIC", "CREATIVE", "OPERATIONAL", "AUDIENCE", "FAILURE"]},
          "entry_id": {"type": "string", "format": "uuid"},
          "relevance_score": {"type": "number", "minimum": 0, "maximum": 1}
        }
      }
    },
    "project_context": {
      "type": "object",
      "required": ["project_id", "thesis_statement", "format_constraints", "deadlines", "quality_bar"],
      "properties": {
        "project_id": {"type": "string"},
        "thesis_statement": {"type": "string", "maxLength": 200},
        "format_constraints": {"type": "array", "items": {"type": "string"}},
        "story_rules": {"type": "string"},
        "research_evidence": {"type": "string"},
        "assets_available": {"type": "array", "items": {"type": "string"}},
        "deadlines": {"type": "object", "additionalProperties": {"type": "string", "format": "date-time"}},
        "quality_bar": {
          "type": "object",
          "required": ["min_omega_score"],
          "properties": {
            "min_omega_score": {"type": "number", "minimum": 0, "maximum": 1},
            "min_truth_score": {"type": "number", "minimum": 0, "maximum": 1},
            "max_risk_score": {"type": "number", "minimum": 0, "maximum": 1}
          }
        }
      }
    },
    "agent_contract": {
      "type": "object",
      "required": ["role", "task", "available_tools", "output_contract_ref", "failure_conditions_ref"],
      "properties": {
        "role": {"type": "string"},
        "task": {"type": "string", "maxLength": 500},
        "available_tools": {"type": "array", "items": {"type": "string"}},
        "relevant_knowledge": {"type": "array", "items": {"type": "string"}},
        "output_contract_ref": {"type": "string"},
        "failure_conditions_ref": {"type": "string"}
      }
    },
    "state_transition": {
      "type": "object",
      "required": ["current_phase", "target_phase"],
      "properties": {
        "current_phase": {"type": "string"},
        "target_phase": {"type": "string"},
        "conditions_met": {"type": "array", "items": {"type": "boolean"}},
        "human_gate_required": {"type": "boolean"},
        "red_team_review_pending": {"type": "boolean"}
      }
    },
    "anti_drift_checks": {
      "type": "object",
      "required": ["max_token_estimate", "context_pollution_score", "last_memory_sync"],
      "properties": {
        "max_token_estimate": {"type": "integer", "maximum": 10240},
        "context_pollution_score": {"type": "number", "minimum": 0, "maximum": 1},
        "last_memory_sync": {"type": "string", "format": "date-time"},
        "thesis_alignment_check": {"type": "boolean"},
        "failure_memory_pin_present": {"type": "boolean"}
      }
    }
  }
}
```

---

## 2. PACKET CONSTRUCTION PROTOCOL

```python
from datetime import datetime, timezone

def build_context_packet(agent_id, task_id, current_state, target_state, memory_refs, output_contract_ref):
    packet = {
        "packet_id": generate_uuid(),
        "version": "1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent_context": {
            "agent_id": agent_id,
            "role": lookup_agent_role(agent_id),
            "task_id": task_id
        },
        "runtime_context": {
            "current_state": current_state,
            "previous_action": get_last_action(task_id),
            "errors": get_active_errors(task_id),
            "dependencies": get_unresolved_dependencies(task_id),
            "next_action_target": target_state
        },
        "memory_pins": format_memory_refs(memory_refs),
        "project_context": build_project_context(task_id),
        "agent_contract": build_contract(agent_id, task_id, output_contract_ref),
        "state_transition": {
            "current_phase": current_state,
            "target_phase": target_state,
            "conditions_met": check_transition_conditions(current_state, target_state),
            "human_gate_required": is_gate_required(current_state, target_state),
            "red_team_review_pending": check_red_team_status(task_id)
        },
        "anti_drift_checks": {
            "max_token_estimate": estimate_token_size(memory_refs, output_contract_ref),
            "context_pollution_score": compute_pollution(memory_refs),
            "last_memory_sync": get_last_memory_sync_time(),
            "thesis_alignment_check": check_thesis_alignment(memory_refs),
            "failure_memory_pin_present": any(ref["bank_id"] == "FAILURE" for ref in memory_refs)
        }
    }

    # Anti-pollution enforcement
    assert packet["anti_drift_checks"]["max_token_estimate"] <= 10240, "Packet exceeds 10KB"
    assert packet["anti_drift_checks"]["context_pollution_score"] <= 0.3, "Pollution too high"
    assert packet["anti_drift_checks"]["failure_memory_pin_present"], "FAILURE pin required"
    assert packet["project_context"]["thesis_statement"], "Thesis statement required"

    return packet
```

---

## 3. CONTEXT POLLUTION DETECTION

```python
def compute_pollution(memory_refs):
    # High pollution = too many unrelated memory pins, missing failure pin,
    # missing strategic reference, missing thesis alignment
    score = 0.0

    # Check diversity of memory banks
    banks = set(ref["bank_id"] for ref in memory_refs)
    if len(banks) < 2:
        score += 0.2  # Too narrow

    # Check failure presence
    if not any(ref["bank_id"] == "FAILURE" for ref in memory_refs):
        score += 0.3

    # Check strategic presence for strategic phases
    if any(ref["bank_id"] == "FAILURE" for ref in memory_refs) and not any(ref["bank_id"] == "STRATEGIC" for ref in memory_refs):
        score += 0.1  # Failure without strategic context

    # Check relevance scores
    avg_relevance = sum(ref.get("relevance_score", 0) for ref in memory_refs) / len(memory_refs)
    if avg_relevance < 0.7:
        score += 0.1

    return min(score, 1.0)
```

---

## 4. PACKET LIFECYCLE

```
CREATE (Master Orchestrator) → VALIDATE (Schema + Anti-Drift) → ASSIGN (Agent)
→ EXECUTE (Agent reads packet, writes to memory) → UPDATE (Agent writes new packet state)
→ SYNCHRONIZE (Memory banks updated) → ARCHIVE (Episodic storage)
```

Packets are archived in `OPERATIONAL_MEMORY` with full history for replay and rollback.
