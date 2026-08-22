# Specification index

This is the canonical engineering specification for Tetrative Agentic OS. Specifications are ordered
by the decision sequence: **intent → product → technical design → contracts → tests → safety →
operations → maintenance**.

## Authority order

When documents conflict, resolve them in this order:

1. Human-approved product and safety requirements.
2. Architecture decision records (ADRs).
3. API/data contracts and state-machine specification.
4. Implementation and tests.
5. Informational/legacy documents.

A test passing does not authorize behavior prohibited by a requirement or safety control. Code that
disagrees with an approved specification is a defect unless an ADR changes the specification.

## Map

| Area | Canonical documents |
|---|---|
| Engineering intent | [`01-engineering-intent/`](01-engineering-intent/) |
| Product requirements | [`02-product-requirements/`](02-product-requirements/) |
| Technical specification | [`03-technical-spec/`](03-technical-spec/) |
| API and data design | [`04-api-and-data-design/`](04-api-and-data-design/) |
| Test specification | [`05-test-specification/`](05-test-specification/) |
| Security and reliability | [`06-security-and-reliability/`](06-security-and-reliability/) |
| Deployment and monitoring | [`07-deployment-and-monitoring/`](07-deployment-and-monitoring/) |
| Maintenance and drift | [`08-maintenance-and-spec-drift/`](08-maintenance-and-spec-drift/) |
| Executable work queue | [`../tasks/agent-task-list.md`](../tasks/agent-task-list.md) |
| Human/agent review log | [`../tasks/review-notes.md`](../tasks/review-notes.md) |
| Change history | [`../changelog/CHANGELOG.md`](../changelog/CHANGELOG.md) |

The older top-level documents remain useful deep dives. Their normative requirements are progressively
being migrated into this numbered specification.

## The one rule

> Before code, write or identify the requirement and acceptance test. Before acceptance, run the
> tests and review safety. Before release, record the change. After release, update the specification
> when observed reality invalidates an assumption.
