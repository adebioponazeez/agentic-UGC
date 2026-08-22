# Evaluation, stress testing, and self-evolution

## Balanced scorecard

Do not optimize a single synthetic score. Release decisions use hard safety gates plus a scorecard:

| Dimension | Example measure | Initial gate |
|---|---|---:|
| Truth/provenance | supported factual claims | ≥ 95% |
| Goal relevance | rubric score from blinded cases | ≥ 0.80 |
| Execution | acceptance tests that are runnable | ≥ 0.85 |
| Robustness | adversarial suite pass rate | ≥ 0.90 |
| Human value | expert pairwise preference | ≥ 60% vs baseline |
| Cost | verified outcome per naira/dollar | improve vs baseline |
| Latency | time to approved artifact | domain SLO |
| Safety | critical policy violations | exactly 0 |
| Calibration | confidence vs observed success | ECE ≤ 0.10 |

The MVP's lexical evaluator is only a control-flow scaffold. Production must use task-specific
programmatic checks, blinded human review, outcome telemetry, and calibrated model judges.

## Continuous stress suites

1. **Truth attacks:** false premises, stale facts, fake citations, source conflicts.
2. **Prompt attacks:** direct/indirect injection in webpages, files, memories, and tool results.
3. **Identity attacks:** unauthorized likeness, voice, testimonials, or brand claims.
4. **Execution attacks:** destructive commands, hidden spend, credential exfiltration, race conditions.
5. **Market attacks:** vanity demand, survivorship bias, competitor response, channel saturation.
6. **Creative attacks:** generic hooks, cultural mismatch, continuity errors, deceptive editing.
7. **Governance attacks:** colluding graders, rubric gaming, approval bypass, poisoned memory.
8. **Scale attacks:** 10× load, 1,000× audience, cost spikes, provider outage, model regression.

Every production incident becomes a minimized regression case. Sensitive cases are redacted before
entering shared eval datasets.

## Debate without theater

Multi-agent debate is useful only when it adds independent evidence or catches errors. Measure it
against a single-agent baseline. Disable extra agents for task classes where they increase cost but
not calibrated quality. Diversity should come from role, evidence, model, temperature, or search
strategy—not renamed copies of one prompt.

## Safe self-improvement loop

```text
Observe outcomes
  → attribute cautiously
  → mine failure/success candidates
  → redact and deduplicate
  → propose prompt/router/tool/memory change
  → run offline regression + adversarial suites
  → shadow deployment
  → canary with rollback
  → human release approval
  → version and monitor
```

Agents may **propose** changes. They may not silently replace their own system prompts, evaluators,
permissions, or release thresholds. A champion/challenger registry stores versions and results.

## Anti-Goodhart rules

- Keep hidden holdout evals.
- Rotate adversarial cases and judges.
- Audit outcome metrics for manipulation and distribution shift.
- Pair engagement with trust, complaints, conversions, refunds, retention, and harm indicators.
- Never treat self-critique length or agent consensus as quality.
- Periodically require evidence from real users and real-world execution.
