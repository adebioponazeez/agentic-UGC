# Deployment, monitoring, and incidents

Local → CI → sandbox → shadow → canary → production. Pin model, prompt, workflow, policy, schema, and
tool versions. Production uses authenticated API, durable runtime, isolated workers, provider router,
Postgres, artifact store, secret manager, policy engine, and OpenTelemetry.

Telemetry includes run/stage transition and versions; provider/model cost and latency; evaluator
versions and dissent; approval digest and actor; tool effects and idempotency; memory evidence IDs.
Secrets and raw sensitive prompts are excluded by default.

Incident sequence: detect → stop provider/tool → preserve evidence → contain → assess → rollback →
notify as required → create regression case → update threat model, tests, and changelog. An agent
cannot close its own safety incident.
