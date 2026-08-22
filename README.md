# Tetrative Agentic OS

A provider-agnostic, local-first cognitive orchestration kernel for **agentic UGC**, a reusable
**Meta-Orchestrator**, and an AI-native **venture operating system**.

> “Billion-by-billion-fold tetrative intelligence” is treated as a direction, not a fake benchmark.
> Capability cannot be responsibly multiplied by saying it is. This system compounds **parallel
> exploration × adversarial selection × tool leverage × reusable memory × iteration speed**, while
> bounding cost, risk, and recursion.

## What is implemented

- Four executable workflows: `meta`, `ugc`, `venture`, and an integrated `ecosystem` run
- Role-separated agents with explicit mandates and least-privilege tool declarations
- Best-of-N candidate generation
- Red-team cross-examination on every candidate
- Hybrid evaluation and bounded revise/retry loops
- Human approval gates before consequential execution
- Versioned SQLite schema, durable checkpoints, approval audit, events, and lesson memory
- Spec-first workspace with traceable requirements, state contracts, tests, threats, tasks, and releases
- Local model support through any OpenAI-compatible endpoint (Ollama, vLLM, llama.cpp)
- Deterministic offline mode for CI and architecture demos
- JSON run artifacts suitable for dashboards, audits, and later training/evaluation

## Quick start

Requires Python 3.11+ and has no runtime dependencies.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .

# Prove the full orchestration path without a model server
tetrative "Launch an evidence-led creator ecosystem for Nigerian founders" \
  --domain ecosystem --audience "solo founders in Lagos" --mock --auto-approve \
  --metric "10 paid design partners" --output ecosystem-run.json
```

Local-first real model (example with an already-running Ollama OpenAI-compatible server):

```bash
export TETRATIVE_BASE_URL=http://localhost:11434/v1
export TETRATIVE_MODEL=qwen3:8b
export TETRATIVE_API_KEY=local
tetrative "Create a 30-day founder-led UGC campaign" --domain ugc \
  --audience "African SaaS buyers" --auto-approve --output campaign.json
```

Omit `--auto-approve` in real operations. The run creates a durable checkpoint and prints the digest
of the exact artifact requiring review. Resume it without regenerating approved stages:

```bash
tetrative --resume RUN_ID --approve PRINTED_SHA256 --approver "reviewer@example.com" \
  --mock --memory .tetrative/memory.db --output resumed-run.json
```

The digest protects artifact integrity but does not authenticate the reviewer. Production must place
the API behind authentication, RBAC, signed approvals, and tenant isolation.

## Domains

| Domain | Path |
|---|---|
| `meta` | root diagnosis → capability map → system design → execution plan → synthesis |
| `ugc` | audience truth → creative strategy → content package → production → learning brief |
| `venture` | problem-market → evidence → thesis → product/GTM → operations → board memo |
| `ecosystem` | diagnosis → intelligence architecture → venture engine → UGC engine → agentic OS → charter |

## Tests

```bash
python -m pytest -q
# Or, with no pytest installation (when not installed editable):
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Engineering documents

- **[Canonical specification index](docs/README.md)**
- [Product requirements and acceptance](docs/02-product-requirements/product-requirements.md)
- [System state machine](docs/03-technical-spec/system-and-state-machine.md)
- [API and data contracts](docs/04-api-and-data-design/contracts.md)
- [Test plan and release gates](docs/05-test-specification/test-plan.md)
- [Threat model](docs/06-security-and-reliability/threat-model.md)
- [Agent task list](tasks/agent-task-list.md)
- [Changelog](changelog/CHANGELOG.md)

Supporting deep dives:

- [System architecture](docs/ARCHITECTURE.md)
- [Agent prompts and protocols](docs/AGENT_PROTOCOLS.md)
- [Evaluation, stress testing, and evolution](docs/EVALUATION.md)
- [Deployment and roadmap](docs/DEPLOYMENT.md)
- [Global repository benchmark, edge cases, and technical debt](docs/GLOBAL_BENCHMARK.md)

## Safety boundary

Generated output is a proposal, not truth or authorization. Agents cannot approve their own
high-impact actions. Financial transactions, publishing, deletion, external messaging, identity use,
legal claims, and production deployment require scoped tools, policy checks, and human approval.
