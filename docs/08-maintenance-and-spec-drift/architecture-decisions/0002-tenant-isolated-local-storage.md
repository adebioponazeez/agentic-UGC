# ADR-0002: tenant-isolated local storage roots

**Status:** Accepted · **Date:** 2026-08-22

## Context

The v0.3 service used one bearer key and one SQLite/artifact root. It could not distinguish operators
from approvers or prevent cross-customer lookup in a shared service.

## Decision

Resolve bearer keys to server-side principals and enforce route roles. Use a distinct SQLite database
and content-addressed artifact root per tenant for the local/single-server runtime. Approval actor is
the authenticated principal subject.

## Consequences

Isolation is easy to inspect and test, and existing single-user behavior maps to a `default` tenant.
Cross-tenant analytics and shared memory are intentionally unavailable. This does not replace
production identity federation, database row-level security, or object-store IAM. A future Postgres
adapter must preserve the principal contract while replacing directory isolation with transactional
row policies.
