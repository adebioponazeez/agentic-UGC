# Agent task list

| ID | Status | Priority | Task | Requirements | Evidence | Gate |
|---|---|---:|---|---|---|---|
| T-001 | Done | P0 | Establish numbered spec workspace | All | Index/specs/tests | Human review |
| T-002 | Done | P0 | Durable digest-bound resume | FR-005–009 | Unit + CLI journey | Human |
| T-003 | Done | P0 | Provider resilience controls | FR-004 | Runtime tests | Engineering |
| T-004 | Done | P0 | Version checkpoints and DB migration | INV-009, NFR-008 | Compatibility tests | Engineering |
| T-005 | Partial | P0 | Domain quality/safety eval gates | TD-001 | Dataset + hard failures | Product/safety |
| T-006 | Partial | P0 | Typed tool capability registry | FR-012 | Sandbox/policy tests | Security/human |
| T-007 | Done | P0 | Grounded research adapter | FR-013 | Citation tests | Research |
| T-008 | Ready | P1 | OpenTelemetry exporter | TD-006 | Trace/redaction tests | Operations |
| T-009 | Ready | P1 | Durable multi-worker adapter | TD-005 | Crash/race/lease tests | ADR |
| T-010 | Ready | P1 | Memory lifecycle controls | TD-008 | Poison/expiry/delete tests | Privacy |
| T-011 | Done | P0 | Authenticated operator API and web console | FR-005–011 | API journey tests | Operations |
| T-012 | Done | P1 | Integrity-verifiable UGC package exporter | FR-014 partial | ZIP manifest tests | Human publish gate |
| T-013 | Done | P1 | Local, server, and cloud deployment references | NFR-004–008 | Docker/K8s configs | Operations |
| T-014 | Done | P0 | API principal, RBAC, and tenant isolation | FR-015–017 | Role/tenant boundary tests | Security |
| T-015 | Partial | P1 | Structured request tracing | TD-006 | Request IDs and JSON events | Operations |
| T-016 | Done | P0 | Deterministic critical policy gates and fail-closed stopping | FR-018–019 | Policy/remediation tests | Product/safety |
| T-017 | Done | P0 | V220 strategic outcome contracts and three-horizon plans | OUT-001–004 | Engine/API tests | Strategy |
| T-018 | Done | P0 | Observation-driven trajectory recalibration | OUT-005–009 | Recalibration/evidence tests | Outcome owner |
| T-019 | Done | P0 | High bounded-autonomy authorization controller | Autonomy envelope | Allow/approve/deny tests | Security/human |
| T-020 | Done | P1 | Outcome, observation, decision, and action ledgers | OUT-007–008 | DB v1→v2 migration tests | Engineering |
