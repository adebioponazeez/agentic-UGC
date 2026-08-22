# Identity, roles, and tenant isolation

**Status:** Implemented for API-key principals · **Version:** 1.0

## Principal contract

Every authenticated API key resolves server-side to an immutable principal:

```json
{
  "subject": "reviewer-123",
  "tenant": "acme",
  "roles": ["viewer", "approver"]
}
```

Clients cannot assert or override subject, tenant, or roles in request bodies. Approval identity comes
from the authenticated principal, not user-entered text.

## Roles

| Role | Permissions |
|---|---|
| `viewer` | List/read tenant runs and download tenant artifacts |
| `operator` | Create runs, collect research, and export packages |
| `approver` | Approve the exact gated artifact and resume a run |
| `admin` | All permissions within one tenant |

Roles do not cross tenants. A key belongs to exactly one tenant in v1.

## Local isolation model

Each tenant has a separate root:

```text
TETRATIVE_DATA_DIR/tenants/{tenant}/
  memory.db
  artifacts/
```

Tenant identifiers are restricted to 1–64 ASCII letters, numbers, underscores, and hyphens. API
handlers derive all storage paths from the authenticated principal. Artifact IDs and run IDs from
another tenant therefore resolve as not found.

This provides strong simple isolation for local and single-server operation. On first v0.4 startup,
legacy v0.3 `memory.db` and `artifacts/` are atomically moved into the `default` tenant only when the
target is empty; existing tenant data is never overwritten or merged. Cloud production should use
database row-level security, tenant-scoped object-store policies, tenant-aware encryption keys, and
adversarial authorization tests rather than depending only on directory boundaries.

## Configuration

Preferred configuration is `TETRATIVE_API_KEYS_JSON`, an object keyed by bearer secret. Each value
contains `subject`, `tenant`, and `roles`. A legacy `TETRATIVE_SERVER_API_KEY` creates one local admin
principal for migration and single-user deployments. Production keys require at least 24 characters.

Keys are credentials: do not commit, log, return, hash into artifact metadata, or place in model
context. Rotate by adding the replacement, deploying, then removing the old key after active clients
migrate.
