# Strategic outcome contract

**Status:** Implemented baseline · **Schema:** `strategic.outcome.v220`

An outcome contract contains:

- north-star statement and accountable owner;
- one primary metric with unit, baseline, target, and maximize/minimize direction;
- 30-day, 365-day, and 1,460-day horizon milestones;
- capital and risk budgets;
- non-negotiable guardrails;
- candidate bets with impact, confidence, cost, reversibility, evidence, and kill criteria;
- bounded-autonomy envelope;
- observations and recalibration decisions.

## Requirements

| ID | Requirement |
|---|---|
| OUT-001 | Reject outcomes without numeric baseline, target, unit, owner, or meaningful direction. |
| OUT-002 | Materialize all three planning horizons while respecting the final target. |
| OUT-003 | Rank and allocate candidate bets without exceeding the capital envelope. |
| OUT-004 | Every bet has a falsifiable kill criterion and an accountable owner. |
| OUT-005 | Record observations with time, metric, value, note, and optional evidence artifact. |
| OUT-006 | Recalibrate trajectory into amplify, continue, adapt, or pivot/stop. |
| OUT-007 | Preserve every allocation and recalibration decision in the audit ledger. |
| OUT-008 | Link agent runs and action proposals to the outcome contract. |
| OUT-009 | Never infer real-world progress from model output; only observations move the metric. |

## Strategic status

`active`, `ahead`, `on_track`, `behind`, `critical`, `paused`, `achieved`, and `stopped` are legal
states. Only observed metric evidence may produce `achieved`.
