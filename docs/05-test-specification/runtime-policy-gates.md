# Runtime policy and domain gates

**Status:** Implemented baseline · **Version:** 1.0

Quality scoring and policy authorization are separate. A high quality score cannot cancel a blocking
policy finding. Every finding has a stable rule ID, severity, message, and remediation.

## Baseline rules

| Rule | Applies when | Result |
|---|---|---|
| POL-001 | Output explicitly recommends bypassing human approval or safeguards | Block |
| POL-002 | Output recommends impersonation or likeness/voice cloning without consent | Block |
| POL-003 | Grounded run output uses supplied evidence but has no `[S#]` citation | Block |
| UGC-001 | UGC production plan omits rights/consent/licensing controls | Block |
| UGC-002 | UGC production plan omits synthetic/sponsored disclosure consideration | Block |
| RISK-001 | High/critical-risk execution plan omits human approval | Block |
| RISK-002 | High/critical-risk execution plan omits stop/rollback/escalation | Block |
| CLAIM-001 | Output uses absolute guarantee language | Warn |

Rules are intentionally narrow and deterministic. They do not attempt semantic content moderation or
replace domain experts. False positives and bypasses become versioned adversarial fixtures.

## Selection and stopping

Candidates without blockers rank ahead of blocked candidates regardless of quality score. A blocked
candidate enters the bounded revision loop even when its score passes. If all revisions remain
blocked, the stage and run stop as `blocked_by_policy`; downstream stages and tools do not execute.
There is no model-controlled override. A future human exception mechanism requires authenticated
policy authority, reason, expiry, and immutable audit—not a prompt instruction.

## Release evolution

Rule changes require frozen regression cases covering positive, negative, quoted/discussion context,
and obfuscation cases. Domain quality still requires human baselines, factuality datasets, and hidden
holdouts; this baseline only establishes enforceable critical gates.
