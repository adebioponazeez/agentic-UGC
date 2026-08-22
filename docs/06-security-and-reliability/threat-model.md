# Threat model

**Status:** Active · **Version:** 1.0

Protected assets: identity, credentials, personal data, strategy, evidence, media rights, budget,
external accounts, approval authority, audit history, and model/tool integrity.

| Threat | Current control | Production control |
|---|---|---|
| Indirect injection | Untrusted delimiters/limits | Taint/provenance and policy |
| Approval spoofing | Digest/non-empty identity | Auth, RBAC, signatures, expiry, four-eyes |
| Stale execution | Run/stage/content digest | Recheck policy/digest at execution |
| Secret leakage | No tool secrets | Secret broker, redaction, egress policy |
| Memory poisoning | Bounded retrieval | Evidence, quarantine, decay, review |
| Judge gaming | Role separation | Diverse graders, holdouts, hard gates |
| SSRF | HTTP(S) validation | Endpoint allowlist/network policy |
| Duplicate effect | No effect tools | Idempotency and outbox |
| Cross-tenant leak | Single-user MVP | Scoped auth/query/encryption tests |
| Audit tampering | Local records | Signed append-only export |

The system may draft high-impact actions but cannot execute them. Enabling a side-effect tool without
INV-007 controls is a release-blocking defect.
