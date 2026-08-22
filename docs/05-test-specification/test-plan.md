# Software and agent test plan

**Status:** Active · **Version:** 1.0

| Layer | Purpose | Location |
|---|---|---|
| Unit | Models, limits, transitions, adapters | `tests/unit/` |
| Integration | CLI, SQLite, HTTP boundary | `tests/integration/` |
| End-to-end | Full workflow and pause/resume | `tests/end_to_end/` |
| Adversarial | Injection, corruption, abuse, bypass | `tests/adversarial/` |
| Evaluation | Grounding, quality, safety, preference | Future eval registry |

Required cases include invalid goals/workflows; stale approval; malformed/oversized/empty provider
responses; timeout, retry, circuit, budget; migration, lock, duplicate approval, interruption; prompt
injection; and critical safety failure despite aggregate quality.

The lexical score verifies orchestration only. Production quality requires domain datasets, grounding,
blinded review, hidden holdouts, calibration, and hard critical-failure gates.

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src tests
git diff --check
```
