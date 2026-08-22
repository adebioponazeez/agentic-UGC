# High bounded-autonomy envelope

**Status:** Implemented authorization baseline · **Version:** 220

High autonomy means many low-risk decisions can proceed without repeated human interruption **inside a
pre-approved envelope**. It does not mean unlimited authority.

An action proposal declares tool, outcome, risk, estimated spend, reversibility, external effect,
idempotency key, and expected/rollback effects. The controller returns `allow`, `require_approval`, or
`deny` with stable reasons.

## Hard decisions

- Deny when kill switch is active, tool is not allowed, risk exceeds ceiling, spend exceeds remaining
  budget, idempotency is absent for external effects, or rollback is absent for reversible effects.
- Require approval for irreversible actions and protected categories: payments, publishing, identity,
  external messaging, deletion, contracts, credential changes, and production deployment.
- Allow only when capability, risk, spend, reversibility, and rate limits fit the envelope.

Authorization is not execution. A tool still validates schema, capability, policy, idempotency, and
current approval at effect time. Decisions expire when the outcome or authority envelope changes.
