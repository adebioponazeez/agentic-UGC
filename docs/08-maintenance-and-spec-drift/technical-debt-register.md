# Technical-debt register

| ID | Debt | Priority | Exit evidence |
|---|---|---:|---|
| TD-001 | Lexical quality scaffold is gameable | P0 | Domain evals, hard safety gates, calibration |
| TD-002 | API-key RBAC exists; no federation/row-level tenancy | P0 | OIDC, RLS, rotation and authorization suite |
| TD-003 | No typed side-effect tool registry | P0 | Capability/idempotency/rollback tests |
| TD-004 | Research is not citation-grounded | P0 | Claim/evidence and source snapshot tests |
| TD-005 | SQLite is single-process durability | P1 | Lease-safe durable runtime adapter |
| TD-006 | No OTel export | P1 | Trace and redaction integration tests |
| TD-007 | No token/currency budget | P1 | Provider accounting and hard cost gate |
| TD-008 | Memory lacks provenance/decay/deletion | P1 | Lifecycle and poisoning suite |
| TD-009 | No multimodal rights pipeline | P2 | Asset/consent/continuity checks |
| TD-010 | No outcome experiment service | P2 | Holdout/sequential tests |

See [`../GLOBAL_BENCHMARK.md`](../GLOBAL_BENCHMARK.md) for the detailed inventory.
