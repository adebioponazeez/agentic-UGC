# Kubernetes deployment

The manifest demonstrates cloud scheduling and security posture, but SQLite on a `ReadWriteOnce` PVC
is **not valid for two active replicas**. Before scaling above one replica, implement TD-005 using
Postgres plus a durable workflow runtime and replace the PVC state adapter. Set `replicas: 1` for the
current implementation. Create `tetrative-secrets` out of band; never commit secret values.
