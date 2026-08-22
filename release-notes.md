# Release notes

## v220.0.0 — strategic outcome operating system

Version 220 changes the system's optimization target from agent output to observed strategic outcomes.
It introduces numeric outcome contracts, three simultaneous planning horizons, reversible option
portfolios, budget-constrained allocation, evidence-only metric movement, continuous trajectory
recalibration, and high bounded-autonomy action authorization.

The new `/api/v220/outcomes` surface and operator console manage portfolios, observations, decisions,
actions, and outcome-linked cognition runs. Database schema v2 preserves previous run data while
adding immutable strategic ledgers. Application and workflow versions intentionally jump to 220.0.0;
this denotes an architecture generation, not a fabricated intelligence benchmark.


## v0.5.0 — deterministic critical policy gates

Quality and authorization are now separate. Stable deterministic rules block approval bypass,
unauthorized identity simulation, uncited grounded outputs, incomplete UGC rights/disclosure plans,
and high-risk plans without human approval and rollback. Blocked candidates enter bounded remediation;
if blockers remain, the run stops as `blocked_by_policy` and no downstream stage executes.

Policy findings travel with candidates, checkpoints, events, metrics, API responses, and the operator
console. This baseline is intentionally narrow and does not replace domain factuality datasets,
calibrated model evaluation, or human safety review.


## v0.4.0 — identity and tenant boundary

- Bearer credentials now resolve server-side to immutable subject, tenant, and role principals.
- Viewer, operator, approver, and admin permissions are enforced by route.
- Approval actor is derived from authentication rather than client-entered text.
- Each local tenant receives an isolated database and artifact root.
- Cross-tenant run and artifact access returns not found.
- Preferred multi-principal configuration uses `TETRATIVE_API_KEYS_JSON`.
- Every HTTP response receives a request ID and emits a secret-free structured audit event.

This is production-oriented service authentication, but not yet OIDC/SSO, database row-level security,
or distributed policy enforcement. Those remain explicit cloud-scale gates.


## v0.3.0 — real operator vertical slice

Tetrative is now an operable application rather than only a CLI orchestration kernel.

### Operator experience

- Responsive web console and versioned FastAPI service.
- Durable run ledger, stage inspection, exact human approval, and continuation.
- Development mock mode and configured OpenAI-compatible local/cloud model mode.

### Grounded venture research

- Collect 1–10 user-selected public HTTPS sources.
- Block unsafe schemes, credentials, ports, private/reserved DNS results, and unsafe redirects.
- Preserve immutable raw snapshots, content hashes, retrieval timestamps, extracted text, and `[S#]`
  citation IDs in content-addressed storage.
- Attach a bounded evidence bundle to venture, UGC, meta, or integrated ecosystem runs.
- Apply a citation-grounding evaluator dimension when evidence is attached.

### UGC production delivery

- Export reviewed or completed UGC/ecosystem runs as ZIP packages.
- Include each selected stage artifact, operator README, workflow/schema versions, approval digest, and
  per-file SHA-256 manifest.
- Verify artifact integrity on every download.

### Platform and deployment

- Fail-closed typed tool registry with capabilities, exact input keys, approval, idempotency, and
  dry-run-only side-effect enforcement.
- Docker Compose for local/single-server operation.
- Single-replica Kubernetes reference with non-root, read-only, probe, resource, and secret controls.
- Explicitly blocks horizontal scaling claims until SQLite is replaced by durable distributed state.

### Validation

The release has unit, API integration, CLI process, research bundle, UGC export, end-to-end,
adversarial network policy, artifact tamper, tool policy, and specification integrity coverage.
