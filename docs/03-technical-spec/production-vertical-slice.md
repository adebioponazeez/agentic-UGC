# Production vertical slice v0.3

**Status:** Implemented for local/single-server use · **Version:** 0.3.0

## Delivered path

```text
public source URLs → SSRF-filtered snapshots → evidence bundle → grounded goal
  → venture/UGC/ecosystem workflow → exact human gate → resumed result
  → integrity-verifiable UGC ZIP
```

The web console and REST API operate the same durable kernel as the CLI. API routes are under
`/api/v1`; `/healthz` is public; all business and artifact routes require a bearer key.

| Method | Route | Purpose |
|---|---|---|
| GET | `/healthz` | Liveness and database schema |
| GET/POST | `/api/v1/runs` | List or create durable runs |
| GET | `/api/v1/runs/{id}` | Checkpoint, outputs, and event history |
| POST | `/api/v1/runs/{id}/approve` | Digest-bound human continuation |
| POST | `/api/v1/research` | Snapshot 1–10 user-selected public HTTPS sources |
| POST | `/api/v1/runs/{id}/exports/ugc` | Build manifest-backed production ZIP |
| GET | `/api/v1/artifacts/{id}` | Integrity-checked artifact download |

## Grounded research controls

Only HTTPS port 443 is accepted. Embedded credentials and DNS answers in private, loopback,
link-local, multicast, unspecified, or reserved ranges are blocked. Redirect destinations are
revalidated. Response types and size are bounded. Raw snapshots are content-addressed; extracted text
is preserved with URL, retrieval time, content hash, citation ID, and snapshot artifact ID.

This is not a truth oracle or search engine. DNS rebinding cannot be completely eliminated by
application checks; production egress must use a network proxy/allowlist. Copyright, robots,
contractual access, retention, and personal-data policy remain operator responsibilities.

## Tool policy kernel

`ToolRegistry` validates registered name, exact input keys, capability, approval, idempotency, and
side-effect class. The v0.3 release deliberately rejects non-dry-run external side effects. This makes
tool contracts executable without prematurely enabling publishing, messaging, payments, or deletion.

## Deployment profiles

- **Local:** `tetrative-api` or Docker Compose, mock or local OpenAI-compatible model.
- **Single server:** production environment, long random bearer key, persistent volume, TLS reverse
  proxy, backups, restricted egress.
- **Cloud:** Kubernetes reference manifest with non-root/read-only security context and probes.
  Current SQLite adapter requires one replica. Horizontal scaling is blocked until Postgres and a
  durable worker/lease runtime replace it.

## Honest limitations

Runs execute synchronously in API worker threads; shared bearer key is service authentication, not
multi-user RBAC; source collection is user-directed; UGC export contains reviewed production
instructions/scripts rather than generated video; model quality still needs domain eval gates. These
are explicit release boundaries, not hidden claims.
