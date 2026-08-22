# Version 220 strategic outcome API

All routes are tenant-scoped and require viewer/operator authorization as appropriate.

| Method | Route | Purpose |
|---|---|---|
| POST | `/api/v220/outcomes` | Create contract, three horizons, and ranked capital allocation |
| GET | `/api/v220/outcomes` | List tenant outcome portfolios |
| GET | `/api/v220/outcomes/{id}` | Contract, plan, observations, decisions, and action ledger |
| POST | `/api/v220/outcomes/{id}/observations` | Record real metric evidence and recalibrate |
| POST | `/api/v220/outcomes/{id}/actions/authorize` | Evaluate proposal against autonomy envelope |
| POST | `/api/v220/outcomes/{id}/kill-switch` | Approver pauses/reactivates linked autonomy |
| POST | `/api/v1/runs` with `outcome_id` | Launch a linked advisory/execution cognition run |

## Outcome persistence

Database schema v2 adds `outcomes`, `outcome_observations`, `outcome_decisions`, and `action_ledger`.
The v1→v2 migration is transactional and preserves run events, lessons, checkpoints, and approvals.

## Integrity rules

- Creating an outcome records its initial plan as a decision.
- Observing the primary metric creates a recalibration decision and updates strategic status.
- Reaching the numeric target is not `achieved` until a tenant-scoped evidence artifact is attached.
- Linked model runs are decision evidence only and never increment the metric.
- Reusing an action idempotency key returns the original decision only for an identical proposal;
  changed content with the same key returns conflict.
- Authorization decisions are immutable ledger entries and are not themselves tool execution.
