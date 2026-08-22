# Deployment and evolution roadmap

## MVP (implemented)

Single Python process, OpenAI-compatible model adapter, SQLite memory, JSON artifacts, bounded
best-of-N evaluation loops, and CLI human checkpoints.

## Production reference architecture

- **API/control plane:** FastAPI or equivalent; typed goal and artifact schemas.
- **Workflow runtime:** Temporal, durable execution, or equivalent for resumable DAGs and approvals.
- **Workers:** isolated pools by tool risk; egress allowlists and per-task credentials.
- **Models:** policy router across local and external providers; no provider-specific business logic.
- **Storage:** Postgres for state/RBAC, object store for hashed artifacts, vector/keyword retrieval.
- **Observability:** OpenTelemetry traces, token/cost ledger, eval dashboards, immutable audit events.
- **Policy:** OPA/Cedar-style authorization, tenant boundaries, consent and retention rules.
- **Delivery:** sandbox → shadow → canary → production with automatic rollback.

Local models should handle classification, extraction, drafting, and sensitive workloads when quality
passes. Larger remote models may be routed to difficult synthesis tasks only with data-policy
permission. Record provider, model digest, prompt version, tools, and seed where available.

## Security baseline

- Treat all retrieved content and memory as untrusted data, never instructions.
- Separate planning from execution; use schema-valid tool calls.
- Use ephemeral, least-privilege credentials; never expose secrets to general model context.
- Sandbox code/media processing with CPU, memory, time, file, and network limits.
- Require idempotency keys and dry runs for external side effects.
- Encrypt in transit/at rest and support deletion/retention obligations.
- Verify artifact hashes at approval and execution time.
- Maintain emergency stop, provider kill switches, and manual rollback.

## Roadmap

### Phase 1 — reliable vertical slice (0–30 days)

- Add JSON Schema/Pydantic artifacts and schema repair.
- Add resumable signed approval endpoint and minimal operator UI.
- Add budget/cost/token controls and provider fallback router.
- Implement a real UGC campaign case with source citations and outcome ingestion.
- Establish 100-case baseline plus prompt-injection and identity-safety suites.

### Phase 2 — tool-grounded execution (31–90 days)

- Browser/research adapter with citation verification.
- Media asset, code sandbox, publishing preview, and analytics connectors.
- Durable workflow runtime, RBAC, tenancy, and full traces.
- Champion/challenger prompt and model registry.
- Causal experiment templates: holdouts, incrementality, and stopping rules.

### Phase 3 — portfolio compounding (3–12 months)

- Knowledge graph and outcome-weighted retrieval.
- Automatic workflow induction from successful traces, gated by regression tests.
- Cross-venture component marketplace with privacy-preserving boundaries.
- Learned router optimizing Pareto frontiers of quality, risk, latency, and cost.
- Simulation environments for market, operational, and adversarial rehearsal.

### Toward 2029–2030

Remain model-agnostic. Increase autonomy only when empirical reliability and governance justify it.
Move from static agent names toward dynamically assembled capability graphs, formally verified tool
contracts, richer world models, continuous simulation, and cryptographically attributable media.
Human authority over identity, values, high-impact resource allocation, and irreversible action
remains a design invariant rather than a temporary limitation.
