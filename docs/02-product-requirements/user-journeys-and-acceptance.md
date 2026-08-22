# User journeys and acceptance criteria

**Status:** Draft · **Version:** 1.0

## J-001: offline architecture run

Operator supplies a valid goal. Mock mode executes every declared stage and persists a JSON result.

**Acceptance:** `completed`; stages appear once in order; metrics/events exist; no network required.

## J-002: reviewed UGC run

System pauses at `production_plan`; reviewer supplies run ID, exact digest, and identity; execution
resumes at `learning_brief`.

**Acceptance:** approved stages are not regenerated; wrong digest is rejected; run ID is preserved;
approval appears in the event log.

## J-003: provider degradation

Transient failures retry within policy; repeated failures open the circuit.

**Acceptance:** counts are accurate; no provider call after circuit opening; failed run checkpoints;
secrets and raw provider bodies are not added to events.

## J-004: high-impact action request

A goal asks to publish, spend, impersonate, delete, or contact external people.

**Acceptance:** MVP may draft a plan but has no side-effect tool. Future execution remains blocked
until typed capability, policy, identity, idempotency, and approval controls pass.

## Release acceptance

- Unit, integration, end_to_end, and adversarial tests pass.
- Compilation and `git diff --check` pass.
- No open P0 defect or unmitigated critical threat.
- Product/safety owner reviews requirement changes.
- Changelog and affected specifications are updated.
