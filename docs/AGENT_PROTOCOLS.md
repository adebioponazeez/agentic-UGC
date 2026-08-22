# Agent prompts and operating protocols

Canonical executable prompts live in `src/tetrative_os/topology.py`. This document specifies the
shared contract engineers should preserve when prompts evolve.

## Shared system envelope

Every specialist receives:

- role and narrow mandate;
- goal, audience, constraints, risk, and success metrics;
- upstream artifacts and provenance;
- relevant scored lessons, never unrestricted memory dumps;
- available tools and explicit prohibited actions;
- output schema and acceptance rubric;
- instruction to separate facts, assumptions, recommendations, and unknowns.

## Meta-Orchestrator system prompt

```text
You are the control plane, not the source of truth. Decompose the validated goal into a dependency
DAG. Assign each task to the least-privileged competent role. Enforce budgets, schemas, independent
evaluation, and human gates. Never convert uncertainty into confidence by repetition. Preserve
material dissent. Stop when evidence is insufficient, policy blocks action, or expected information
gain is lower than cost. Optimize verified goal progress, not token volume or agent activity.
```

## Cross-examination protocol

The red team must ask:

1. What exact claim would fail first, and what evidence would reveal it?
2. Which premise is merely repeated rather than independently supported?
3. What would a skeptical customer, competitor, regulator, and security engineer object to?
4. How could the metric be gamed or Goodharted?
5. Who can be harmed, excluded, manipulated, impersonated, or exposed?
6. What second-order consequence appears at 10× and 1,000× scale?
7. What cheaper reversible test dominates the proposed action?
8. What result triggers stop, rollback, escalation, or redesign?

The creator cannot grade itself. The red team cannot rewrite the candidate before recording its
attack. The synthesizer must retain unresolved high-severity dissent.

## UGC artifact minimum

- target viewer and moment of need;
- claim/evidence ledger;
- hook variants tied to hypotheses;
- script, shot list, visual continuity notes, caption, CTA;
- platform and accessibility adaptations;
- disclosure, consent, likeness, music, and IP checks;
- measurement plan with holdout or attribution caveat;
- failure/rollback criteria.

## Venture artifact minimum

- painful job and buyer/user distinction;
- current alternatives and non-consumption;
- evidence strength and unknowns;
- wedge, mechanism, offer, distribution path, economics assumptions;
- moat hypothesis without magical thinking;
- 30-day tests, thresholds, kill criteria, and owner;
- security, privacy, legal, and abuse cases;
- operational acceptance tests and rollback plan.

## Stop conditions

Stop recursion when any condition is met:

- quality threshold passes;
- max retries, cost, latency, or context budget is reached;
- consecutive revisions improve less than epsilon;
- evaluators disagree beyond a calibrated threshold;
- required evidence/tool/permission is unavailable;
- a human gate or policy block is reached.
