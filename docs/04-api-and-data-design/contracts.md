# API and data contracts

**Status:** MVP contract · **Schema version:** 1

A Goal requires a non-empty `objective`; supports domain, audience, constraints, metrics, risk, ID,
and timestamp. Domains: `meta`, `ugc`, `venture`, `ecosystem`.

## Run result

```json
{
  "run_id": "uuid",
  "goal": {},
  "status": "completed|awaiting_human_approval|blocked_by_policy",
  "stages": [],
  "final_output": "markdown",
  "metrics": {},
  "started_at": "RFC3339",
  "finished_at": "RFC3339",
  "approval_required": {"stage": "name", "artifact_hash": "sha256"}
}
```

`approval_required` is null unless paused. Every candidate includes `policy_findings`, a list of stable
rule ID, severity, message, and remediation objects. Resume requires run ID, exact SHA-256,
authenticated approver identity, and the same tenant store. Preconditions: checkpoint exists, awaits
approval, versions are supported, and digest matches.

Runtime metrics are cumulative across resume. Character counts are not token or billing metrics.
Adding optional fields is compatible; removing/renaming fields, changing meaning, or changing legal
transitions is breaking. Checkpoint changes require migration.
