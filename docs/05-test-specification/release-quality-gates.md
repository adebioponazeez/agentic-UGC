# Release quality gates

Release fails if any test fails; a critical safety test fails; specification and implementation
conflict; a database change lacks migration tests; a side effect lacks schema, idempotency,
authorization, approval, and rollback; a provider lacks failure/budget tests; a P0 defect remains; or
changelog/task/review evidence is absent.

Model or prompt changes additionally require frozen eval comparison, hidden holdout, cost/latency
report, shadow execution, and rollback to the previous version.
