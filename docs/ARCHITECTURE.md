# Architecture: measurable recursive capability amplification

## 1. Profound-problem diagnosis

The visible request is “increase intelligence by a tetrative scale.” The profound problem is not a
shortage of generated text. It is the gap between **ambition** and **reliably correct action under
uncertainty**.

The core mismatch is:

> Expected outcome: near-unbounded creative and commercial leverage.  
> Current reality: bounded models with incomplete context, unreliable truth calibration, finite tools,
> weak organizational memory, and execution risk.

Blind recursion amplifies error as readily as insight. The system therefore does not pretend to
create literal superintelligence. It seeks multiplicative *effective capability*:

`C_eff = breadth × depth × verification × tool leverage × memory reuse × execution rate × safety`

A zero in verification or safety collapses the product. “Tetrative” is implemented as nested,
bounded compounding loops at four horizons:

1. **Within an answer:** independent candidates → cross-examination → selection → revision.
2. **Within a run:** downstream specialists consume upstream artifacts and expose contradictions.
3. **Across runs:** outcomes become scored lessons, eval cases, reusable components, and routing data.
4. **Across the ecosystem:** successful workflows become versioned templates deployable to new
   products, audiences, and ventures.

## 2. Topology

```text
Human Direction / Ethics / Taste / Approval
                    │
              Goal Contract
                    │
        ┌──────── Meta-Orchestrator ────────┐
        │ DAG scheduler · budget · policy   │
        │ event log · gate controller       │
        └──────────────┬────────────────────┘
                       │
  Diagnostician → Researcher → Strategist → Creator → Operator
       │              │            │           │         │
       └──────────── shared artifact graph / memory ─────┘
                       │
             Red Team ↔ Evaluator
                       │
                  Synthesizer
                       │
              Human approval gate
                       │
       tool-scoped execution / observation
                       │
         telemetry → lessons → eval registry
```

### Control plane

- Validates a typed `Goal` contract.
- Selects a domain workflow and resolves stage dependencies.
- Enforces candidate, retry, cost, time, and approval budgets.
- Records stage transitions and scores in an append-only event stream.
- Prevents generator self-approval through independent evaluator roles.

### Cognitive plane

- **Diagnostician:** root mismatch, causal model, unknowns, falsifiable objective.
- **Researcher:** evidence map, customer truth, counterevidence, provenance.
- **Strategist:** mechanism, positioning, prioritization, constraints, kill criteria.
- **Creator:** audience-native content and product/offer artifacts.
- **Operator:** interfaces, owners, dependencies, acceptance tests, rollback.
- **Red team:** adversarial truth, security, ethics, demand, and feasibility review.
- **Evaluator:** rubric-based selection; no execution authority.
- **Synthesizer:** resolves disagreements into a decision record, preserving dissent.

### Data plane

The MVP uses SQLite:

- **Episodic memory:** immutable events per run/stage.
- **Semantic lessons:** domain, statement, confidence score, and evidence pointer.

Production adds:

- artifact object storage with content hashes;
- relational run state and permissions;
- vector + keyword retrieval, always filtered by tenant and provenance;
- an evaluation registry containing input, expected properties, grader version, and outcome;
- a knowledge graph for goals, claims, evidence, decisions, assets, and observed results.

## 3. Communication protocol

Agents do not conduct unbounded free-form chat. They exchange versioned artifacts:

```json
{
  "artifact_id": "uuid",
  "run_id": "uuid",
  "type": "creative_strategy.v1",
  "producer": "strategist",
  "claims": [{"text": "...", "status": "assumption", "evidence_ids": []}],
  "decisions": [{"choice": "...", "because": "...", "reversible": true}],
  "risks": [{"severity": "high", "mitigation": "..."}],
  "acceptance_tests": [{"metric": "qualified replies", "threshold": 10}],
  "payload": {},
  "content_hash": "sha256"
}
```

Production schemas must reject missing provenance for factual claims and missing rollback plans for
high-risk operations.

## 4. Workflow contract

Every stage follows:

1. Retrieve only relevant, high-confidence memory.
2. Generate N independent candidates with controlled diversity.
3. Run deterministic checks.
4. Red-team each candidate with an attack taxonomy.
5. Independently score against a versioned rubric.
6. Revise below-threshold work within a fixed retry budget.
7. Select, log rationale, and pass a typed artifact downstream.
8. Stop at human gates for consequential actions.
9. Observe real outcomes and update lessons only when evidence exists.

## 5. Human authority

Humans own direction, taste, ethics, identity, and irreversible decisions. Required gates include:

- publishing under a human or brand identity;
- spend, contracts, pricing changes, and financial transactions;
- outreach or collection of personal data;
- legal/medical/financial representations;
- deployment, destructive operations, and credential scope changes;
- training or cloning a real person's likeness or voice.

Approval is a signed decision over an immutable artifact hash, not a vague chat reply.

## 6. Compounding flywheels

### Evidence flywheel

content/product hypothesis → controlled release → behavioral telemetry → causal caveat → scored lesson
→ stronger next hypothesis.

### Component flywheel

high-performing prompt/tool/workflow → regression tests → versioned module → routing catalog → reuse in
new domains.

### Evaluation flywheel

production failures → anonymized hard cases → adversarial eval set → release gate → reduced recurrence.

### Portfolio flywheel

multiple ventures share research infrastructure, creative primitives, distribution learnings, and
operational modules while retaining tenant isolation and consent boundaries.

## 7. Non-goals

- No claims of literal billion-fold model intelligence.
- No autonomous self-modification in production without tests and approval.
- No learning directly from engagement as if engagement implied truth or social value.
- No one-number “intelligence score”; use a balanced, task-specific scorecard.
