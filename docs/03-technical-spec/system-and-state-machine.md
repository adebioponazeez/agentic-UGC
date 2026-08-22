# System and orchestration state machine

**Status:** Accepted for MVP · **Version:** 1.0

## Components

- `models.py`: typed domain records.
- `topology.py`: agent mandates and workflow declarations.
- `orchestrator.py`: transitions, checkpoints, gates, synthesis.
- `runtime.py`: call budget, retry, circuit breaker, telemetry.
- `providers.py`: provider port and local-compatible adapter.
- `evaluation.py`: deterministic scaffold and independent critiques.
- `memory.py`: events, lessons, checkpoints, approvals.
- `cli.py`: local operator interface.

## State machine

```text
NEW → RUNNING → AWAITING_HUMAN_APPROVAL → RUNNING → COMPLETED
          └──────────────────────────────→ FAILED
```

| From | Event | Guard | To | Authority |
|---|---|---|---|---|
| NEW | run | goal/workflow valid | RUNNING | Orchestrator |
| RUNNING | stage complete | dependencies complete | RUNNING | Orchestrator |
| RUNNING | gated stage complete | auto-approve false | AWAITING | Orchestrator |
| AWAITING | approve | status/digest match; approver present | RUNNING | Human boundary |
| RUNNING | final stage complete | no gate/error | COMPLETED | Orchestrator |
| RUNNING | exception | stage/runtime/storage failure | FAILED | Orchestrator |

COMPLETED→RUNNING, FAILED→COMPLETED without recovery, and AWAITING→RUNNING on stale digest are
forbidden. Auto-approval is test/demo behavior, not production authorization.

## Stage algorithm

Resolve dependencies; retrieve bounded lessons; mark context untrusted; generate N candidates;
red-team and judge; revise within limits; select; emit event; checkpoint; stop at gate; record a
provisional lesson only on completion.

## Consistency

SQLite MVP assumes one local writer. It does not claim distributed exactly-once execution. Production
requires worker leases, idempotency, version pins, and transactional outbox semantics. Digest protects
content integrity; CLI approver text is not authentication.
