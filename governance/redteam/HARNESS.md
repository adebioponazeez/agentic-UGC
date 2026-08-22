# QA / RED-TEAM HARNESS v1.0
## Structured adversarial review before any major publication or structural change

---

## 1. RED-TEAM COUNCIL STRUCTURE (OMEGA-M2)

Every major output passes through 10 independent critics:

```
1. CREATIVE CRITIC     (OMEGA-C4) — Is it interesting? Original? Authored?
2. AUDIENCE CRITIC     (OMEGA-P4) — Why would anyone care? Does it serve audience need?
3. FACT CRITIC         (OMEGA-D2) — What is unsupported? What evidence is missing?
4. CINEMATIC CRITIC    (OMEGA-F3) — What looks synthetic, amateur, or generic?
5. RETENTION CRITIC    (OMEGA-C3) — Where does attention collapse? Is retention curve predictable?
6. BUSINESS CRITIC     (OMEGA-P3) — Is there economic value? Is business model durable?
7. POLICY CRITIC       (OMEGA-M4) — Could this create platform, legal, or ethical problems?
8. RIGHTS CRITIC       (OMEGA-E3) — Do we have the rights? Are sources properly attributed?
9. BRAND CRITIC        (OMEGA-0) — Does this damage trust? Is identity consistent?
10. STRATEGIC CRITIC    (OMEGA-D1) — Does this move the larger system forward?
```

---

## 2. REVIEW PROTOCOL

Every review produces structured output:

```json
{
  "review_id": "uuid",
  "review_type": "red_team_council",
  "target_agent_id": "OMEGA-C2",
  "target_output_ref": "scripts/output_42.md",
  "review_timestamp": "ISO8601",
  "critics": [
    {
      "critic_id": "CREATIVE",
      "critic_agent": "OMEGA-C4",
      "score": 0.75,
      "reasoning": "Script has original structure but relies too heavily on generic narration.",
      "recommendation": "REWORK — revise narration to include specific perspective.",
      "evidence": "Line 23: generic description of market dynamics."
    },
    {
      "critic_id": "TRUTH",
      "critic_agent": "OMEGA-D2",
      "score": 0.92,
      "reasoning": "Claims supported by sources in evidence collection.",
      "recommendation": "PUBLISH — evidence adequate.",
      "evidence": "Sources: 3 peer-reviewed papers, 2 industry reports."
    }
  ],
  "aggregate_omega_score": 0.68,
  "aggregate_recommendation": "REWORK",
  "required_actions": [
    "Revise narration in script",
    "Re-submit to red team within 24 hours"
  ],
  "enforcement_status": "PENDING",
  "human_gate_approval": false
}
```

---

## 3. QUALITY ENGINE INTEGRATION

Every critic applies the 5-score framework to their domain:

```
CREATIVE CRITIC:  C (primary) + P (secondary) + B (tertiary)
AUDIENCE CRITIC:  C (primary) + B (primary) + P (secondary)
FACT CRITIC:       T (primary) + P (secondary) + R (secondary)
CINEMATIC CRITIC:  C (primary) + P (primary) + R (secondary)
RETENTION CRITIC:  C (primary) + B (secondary) + P (tertiary)
BUSINESS CRITIC:   B (primary) + R (primary) + P (secondary)
POLICY CRITIC:     R (primary) + T (secondary) + B (tertiary)
RIGHTS CRITIC:     T (primary) + R (primary) + P (tertiary)
BRAND CRITIC:      C (primary) + R (primary) + B (tertiary)
STRATEGIC CRITIC:  C (primary) + B (primary) + T (secondary)
```

---

## 4. ENFORCEMENT MECHANISM

Red team recommendations are non-decorative. They must be executed:

```
RECOMMENDATION: PUBLISH
  → Execution: Proceed to distribution (with any minor notes applied)
  → Memory: Write success to CREATIVE; write review to OPERATIONAL

RECOMMENDATION: REWORK
  → Execution: Block distribution. Return to design/production phase.
  → Memory: Write failure/rework reason to FAILURE; write review to OPERATIONAL
  → Re-test: Re-submit to red team after fixes applied

RECOMMENDATION: ABANDON
  → Execution: Terminate workflow. Do not distribute. Do not produce further.
  → Memory: Write abandonment reason to FAILURE; write strategic assessment to STRATEGIC
  → Re-invest: Propose alternative approach (new hypothesis) within 48 hours
```

---

## 5. STRESS-TEST ENGINE (OMEGA-M3)

### 5.1 Load Testing
```
Test: Activate 10 agents simultaneously with full context packets
Target: Response time < 30 seconds; no memory corruption; no context pollution
Pass Criteria: All responses within target; memory consistent; packets valid
```

### 5.2 Adversarial Testing
```
Test: Inject malicious or incorrect inputs; test agent resilience
Scenarios: Incorrect memory references, contradictory evidence, missing failure pins,
           oversized packets, unauthorized state transitions
Pass Criteria: Agents detect errors; stop execution; write failure memory; propose fix
```

### 5.3 Failure-Mode Testing
```
Test: Simulate specific failure conditions from FAILURE memory
Scenarios: Recurrence of known errors, new errors similar to past errors,
           cascading failures (one agent error triggers others)
Pass Criteria: New guardrails prevent recurrence; cascading failures contained; rollback works
```

### 5.4 Policy Testing
```
Test: Verify governance rules enforced; verify no unauthorized changes
Scenarios: Agent attempts self-modification, context packet exceeds limit,
           human gate bypassed, red team review skipped
Pass Criteria: Governance guardian intervenes; violation logged; action blocked
```

---

## 6. STRESS TEST REPORT FORMAT

Every test produces:

```json
{
  "test_id": "ST-001",
  "test_type": "adversarial",
  "date": "2026-08-22",
  "engine_agent": "OMEGA-M3",
  "conditions": ["malicious_context_packet", "missing_failure_pin", "oversized_packet"],
  "results": {
    "passed": false,
    "failures": [
      {"condition": "missing_failure_pin", "detected": false, "agent": "OMEGA-C2"}
    ]
  },
  "fixes_applied": [
    {"agent": "OMEGA-0", "fix": "added_failure_pin_validation", "test_result": "passed"}
  ],
  "new_guardrails": [
    {"rule": "all_context_packets_must_contain_failure_memory_pin", "agent": "OMEGA-0"}
  ],
  "memory_updates": ["FAILURE:ST-001", "OPERATIONAL:guardrail_update"],
  "roll_back_reference": "ST-001-rollback"
}
```

---

## 7. RED TEAM EXECUTION CADENCE

```
Before any major publication:  Mandatory (all 10 critics)
Before any structural change: Mandatory (all 10 critics + governance guardian)
Before scale authorization:   Mandatory (strategic + business + policy critics)
Before self-evolution:        Mandatory (all critics + stress test engineer)
Weekly audit:                 Random sample of 10% of outputs reviewed
Monthly full review:          All major outputs + portfolio performance reviewed
```

---

## 8. HUMAN GATE PROTOCOL

Every red team recommendation of `REWORK` or `ABANDON` requires human confirmation before execution.
Every `PUBLISH` on high-priority output requires human confirmation.
Every structural change requires explicit human authorization.

The `Governance Guardian` (OMEGA-M4) logs all gates, approvals, and violations in `OPERATIONAL_MEMORY`.
