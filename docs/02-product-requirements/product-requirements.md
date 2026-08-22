# Product requirements document

**Status:** Draft for human acceptance · **Version:** 1.0

## Users and jobs

| Persona | Primary job | Current pain |
|---|---|---|
| Founder/operator | Turn a venture goal into validated bets and execution plans | Generic strategy and weak evidence |
| Creator/brand lead | Produce platform-native UGC with rights and learning controls | Volume without consistency or attribution |
| AI operations engineer | Run long-lived workflows safely across providers | Non-durable loops, hidden cost, weak auditing |
| Human reviewer | Inspect and approve consequential artifacts | Vague approvals detached from exact content |

## MVP scope

- Typed goals for `meta`, `ugc`, `venture`, and `ecosystem`.
- Deterministic stage workflows using portable model calls.
- Independent candidates, red-team review, scoring, and bounded revision.
- SQLite events, lessons, checkpoints, and approval digests.
- Pause/resume without repeating accepted stages.
- Offline deterministic provider and machine-readable JSON artifacts.

## Functional requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-001 | Reject empty, oversized, or unsupported goals before execution. | Must |
| FR-002 | Resolve workflows in declared dependency order. | Must |
| FR-003 | Run independent red-team and evaluator passes per candidate. | Must |
| FR-004 | Bound candidates, revisions, calls, retries, and response size. | Must |
| FR-005 | Persist state after every completed stage. | Must |
| FR-006 | Stop at human gates except explicit demo/CI auto-approval. | Must |
| FR-007 | Resume only the exact awaiting checkpoint and artifact digest. | Must |
| FR-008 | Record approval identity, digest, stage, and time. | Must |
| FR-009 | Fail closed on corrupt state, wrong approval, budget, or circuit failure. | Must |
| FR-010 | Support OpenAI-compatible local endpoints without runtime packages. | Must |
| FR-011 | Provide authenticated, tenant-scoped API approval. | Production P0 |
| FR-012 | Execute typed tools under capability policy and idempotency. | Production P0 |
| FR-013 | Ground research claims in source snapshots and citations. | Production P0 |
| FR-014 | Build multimodal UGC with consent and rights provenance. | Product P2 |

## Nonfunctional requirements

| ID | Requirement | Initial target |
|---|---|---|
| NFR-001 | Determinism | Same workflow definition yields same state transitions |
| NFR-002 | Recoverability | No accepted stage regenerated after valid resume |
| NFR-003 | Auditability | Every transition and approval has a run/stage event |
| NFR-004 | Portability | Business workflow imports no vendor SDK |
| NFR-005 | Testability | Offline full-domain test with deterministic provider |
| NFR-006 | Security | No enabled external side-effect tools in MVP |
| NFR-007 | Performance | Control overhead under 100 ms/stage excluding I/O |
| NFR-008 | Compatibility | Python 3.11+; checkpoint changes require migration |

## Excluded from MVP

Web UI, autonomous publishing, payments, browser control, voice/face cloning, multi-tenancy,
distributed workers, causal attribution, and automatic prompt optimization.
