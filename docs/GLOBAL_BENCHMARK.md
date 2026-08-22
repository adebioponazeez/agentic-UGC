# Global repository benchmark and technical-debt register

Research snapshot: **2026-08-22**. Popularity is not treated as proof of correctness. The comparison
uses repository documentation, architecture fit, maintenance activity, production controls, and the
specific needs of a local-first UGC/venture operating system.

## Reference repositories

| Repository | Pattern worth adopting | What not to copy blindly |
|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Explicit state graphs, durable execution, interrupt/resume, memory, deterministic control around stochastic nodes | Framework and hosted-stack coupling when this kernel can remain small |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | Typed end_to_end contracts, validated tool interfaces, provider portability, strong Python ergonomics | A general agent SDK does not supply our domain workflows or governance model |
| [CrewAI](https://github.com/crewAIInc/crewAI) | Clear role abstractions and fast multi-agent composition; separation of collaborative crews from precise event-driven flows | Conversation/delegation overhead and hidden nondeterminism for critical execution |
| [Langfuse](https://github.com/langfuse/langfuse) | Open-source traces, evaluations, datasets, prompt versions, cost/latency metrics, OpenTelemetry integration | Operating a full observability platform before traffic justifies it |
| [LlamaIndex](https://github.com/run-llama/llama_index) | Data connectors, retrieval, citation-oriented document workflows | Retrieval abstractions where no corpus exists |
| [Temporal](https://github.com/temporalio/temporal) | Durable timers, retries, idempotency, signals, long-running workflow recovery | Infrastructure weight for the zero-dependency local MVP |
| [DSPy](https://github.com/stanfordnlp/dspy) | Optimize programs against evals rather than hand-tuning prompts forever | Optimizing against weak or gameable metrics |
| [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) | Reproducible, composable agent evaluation and safety testing | Treating offline benchmarks as sufficient production evidence |

## Decision

Do **not** replace this project with a generic framework. Keep the domain-specific control kernel and
add adapters at the edges. Its invariant should be:

> deterministic orchestration, typed state, bounded stochastic cognition, provider portability,
> explicit human authority, and outcome-grounded evolution.

LangGraph or Temporal can later become a durable-runtime adapter. Pydantic can become an optional
strict-schema adapter. Langfuse/OpenTelemetry can consume emitted events. This avoids an irreversible
framework commitment while preserving a migration path.

## Gap analysis

| Capability | Previous state | Current state | Remaining production debt |
|---|---|---|---|
| Human gates | stopped with no continuation | artifact digest + SQLite checkpoint + audited resume | authentication, signatures, RBAC, expiry, four-eyes approval |
| Failure recovery | run aborted | stage failure checkpoint and deterministic state snapshots | automatic resume from failed stage; lease/heartbeat semantics |
| Budgets | retry count only | hard model-call budget, provider retries, circuit breaker, usage telemetry | token and currency budgets from provider usage fields |
| Provider safety | basic URL call | URL/config validation, response schema/size checks, empty-output rejection | streaming, cancellation, rate-limit-aware backoff, provider fallback |
| Prompt injection | memory/context interpolated directly | bounded, explicitly untrusted context delimiters | content classifiers, taint tracking, tool-output provenance |
| Workflow correctness | implicit tuple ordering | startup validation for owners, duplicate stages, dependencies, scores | arbitrary DAG scheduling, conditional edges, parallel nodes |
| Goal validation | accepted blank/unbounded input | normalized objective and cardinality/size limits | strict per-domain goal schemas and policy classification |
| Observability | stage score only | model calls, attempts, failures, retries, character I/O, audit events | OpenTelemetry traces, model token/cost fields, dashboards, SLO alerts |
| Evaluation | lexical scaffold + model critique | unchanged; clearly identified scaffold | highest-priority debt: calibrated domain evals and hidden holdouts |
| Memory | confidence stored from run average | same | evidence validation, decay, deduplication, poisoning defense, deletion |
| Concurrency | single process | single process | SQLite leases, WAL/busy timeout, worker ownership, idempotency keys |
| Tool execution | declarations only | declarations only | typed tool registry, capabilities, sandbox, policy engine, dry run |
| UGC media | textual package | textual package | image/video/audio pipeline, consent ledger, continuity and QC evals |
| Research | prompt only | prompt only | browsing connector, source snapshots, citations, freshness checks |

## Edge-case inventory

### State and concurrency

- process crashes before/after model response or checkpoint commit;
- duplicate delivery, resume, or approval requests;
- two workers race to own the same run;
- workflow definition changes while a historical run is paused;
- SQLite locked, disk full, corrupt, or migrated from an older schema;
- approval occurs against stale content or after policy changed.

### Model and provider

- timeout, malformed JSON, HTTP 429/5xx, empty choices, enormous body;
- model silently changes, ignores JSON mode, or returns a tool call instead of text;
- context overflow after upstream artifacts expand;
- retries duplicate a billable or side-effecting provider request;
- fallback provider has different safety, residency, or context characteristics;
- judge and generator share correlated blind spots or collude through prompt artifacts.

### Evaluation and learning

- verbose/generic output games lexical structure checks;
- model judge prefers its own style or memorized benchmark;
- average quality hides one critical safety failure;
- engagement optimization rewards deception, outrage, or unauthorized likeness;
- memory turns an unverified run summary into a high-confidence lesson;
- stale or poisoned lessons dominate retrieval;
- winner selection ignores variance and evaluator disagreement.

### Security and governance

- indirect prompt injection in research, files, analytics, or stored memory;
- secrets or personal data copied into prompts, logs, or external providers;
- unauthorized publishing, spend, outreach, voice/face cloning, or deletion;
- approver identity spoofing in the CLI;
- cross-tenant retrieval or artifact access;
- path traversal, SSRF, malicious media parsers, and sandbox escape once tools arrive;
- audit events edited by someone with database access.

### UGC and venture domain

- copyrighted music/assets, missing releases, synthetic-media disclosure;
- cultural or language mismatch across Nigerian and global audiences;
- platform aspect ratios, caption safe zones, duration, accessibility, and moderation;
- attribution error, bot traffic, seasonality, tiny samples, and no holdout;
- contradictory brand claims across generated variants;
- inventory/support cannot fulfill a successful campaign;
- customer research fabricates quotes or treats inferred personas as observed users.

## Prioritized debt backlog

### P0 — before external side effects

1. Typed tool registry with capability tokens, JSON schemas, dry-run and idempotency semantics.
2. Authenticated API, tenant isolation, RBAC, signed/expiring approvals, and immutable audit export.
3. Hard policy engine for spend, publish, identity, personal data, and destructive operations.
4. Domain eval suites where critical safety failures override aggregate score.
5. Source-grounded research with citation snapshots and explicit claim/evidence status.

### P1 — before multi-worker production

1. Postgres or durable workflow adapter with leases, heartbeats, retries, and schema migrations.
2. OpenTelemetry event model and Langfuse/Phoenix-compatible exporter.
3. Model routing with rate-limit-aware backoff, residency policy, token/cost budgets, and fallback tests.
4. Version every workflow, prompt, rubric, model, and policy in checkpoints.
5. Memory provenance, expiry/decay, deduplication, poisoning review, and deletion workflows.

### P2 — differentiated product capability

1. Multimodal UGC asset graph and continuity evaluator.
2. Consent, identity, rights, and disclosure ledger for every generated asset.
3. Experiment service for holdouts, sequential tests, and attribution caveats.
4. Outcome-grounded DSPy-style prompt/workflow optimization behind champion/challenger gates.
5. Portfolio component registry with privacy-preserving cross-venture reuse.

## Release rule

No increase in autonomy is accepted because a competitor has the feature or a benchmark score rises.
Each increase requires a threat model, regression suite, shadow run, canary, rollback, and named human
owner. This is the compounding advantage: improvements become evidence-backed reusable controls,
not merely additional agents.
