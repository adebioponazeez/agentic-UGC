# Agent task list

| ID | Status | Priority | Task | Requirements | Evidence | Gate |
|---|---|---:|---|---|---|---|
| T-001 | Done | P0 | Establish numbered spec workspace | All | Index/specs/tests | Human review |
| T-002 | Done | P0 | Durable digest-bound resume | FR-005–009 | Unit + CLI journey | Human |
| T-003 | Done | P0 | Provider resilience controls | FR-004 | Runtime tests | Engineering |
| T-004 | In progress | P0 | Version checkpoints and DB migration | INV-009, NFR-008 | Compatibility tests | Engineering |
| T-005 | Ready | P0 | Domain quality/safety eval gates | TD-001 | Dataset + hard failures | Product/safety |
| T-006 | Blocked | P0 | Typed tool capability registry | FR-012 | Sandbox/policy tests | Security/human |
| T-007 | Ready | P0 | Grounded research adapter | FR-013 | Citation tests | Research |
| T-008 | Ready | P1 | OpenTelemetry exporter | TD-006 | Trace/redaction tests | Operations |
| T-009 | Ready | P1 | Durable multi-worker adapter | TD-005 | Crash/race/lease tests | ADR |
| T-010 | Ready | P1 | Memory lifecycle controls | TD-008 | Poison/expiry/delete tests | Privacy |
