# Agent and tool contract

**Status:** Agent contract accepted; tool execution prohibited pending P0 registry

Agents receive role, goal, audience, constraints, metrics, risk, task, bounded untrusted context,
lessons, tool declarations, and output expectations. They distinguish facts, assumptions,
recommendations, risks, and unknowns. They cannot claim an interview, source, tool call, or deployment
without attached evidence.

## Future tool call

```json
{
  "tool": "publisher.preview.v1",
  "idempotency_key": "run:stage:action",
  "capability": "opaque-short-lived-reference",
  "dry_run": true,
  "input": {},
  "expected_effect": {},
  "rollback": {},
  "approval_artifact_hash": "sha256"
}
```

Tools declare schemas, side-effect class, permissions, destinations, timeout, retry safety,
idempotency, cost ceiling, audit fields, and rollback. Free-form shell, publishing, payment, identity,
and deletion tools are forbidden in production.
