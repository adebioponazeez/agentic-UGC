# Principles and invariants

**Status:** Accepted · **Version:** 1.0

| ID | Invariant | Enforcement |
|---|---|---|
| INV-001 | A generator cannot approve its own consequential output. | Role separation and human gate |
| INV-002 | Model output never directly controls authorization. | Deterministic orchestrator |
| INV-003 | Every recursion has call, retry, and iteration limits. | Runtime and stage limits |
| INV-004 | Approval applies to one immutable artifact digest. | SHA-256 checkpoint digest |
| INV-005 | Retrieved content and memory are untrusted data. | Delimiting and truncation |
| INV-006 | Critical safety failure overrides aggregate quality. | Production evaluator pending P0 |
| INV-007 | Side effects require typed, least-privilege tools and policy. | Tools disabled until registry exists |
| INV-008 | Run history is append-oriented and auditable. | Events; immutable export pending |
| INV-009 | Workflow and schema versions travel with durable state. | Versioned checkpoint contract |
| INV-010 | Learning requires evidence and must be reversible. | Evolution gates; stronger controls pending |

## Decision principles

1. Prefer reversible experiments to confident speculation.
2. Separate observations, sourced facts, assumptions, recommendations, and unknowns.
3. Optimize verified outcome per unit of cost and risk—not agent activity.
4. Add agents only when evidence shows improvement over a simpler baseline.
5. Preserve material dissent rather than averaging it away.
6. Fail closed when permission, evidence, policy, or state integrity is uncertain.
7. Keep the kernel inspectable; integrate heavyweight infrastructure behind ports.
