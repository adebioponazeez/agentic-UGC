# PRIMARY WORKFLOW: BURNING PROBLEM → YOUTUBE SERIES + DIGITAL PRODUCT + AGENTIC MVP
## End-to-end execution path for the core value loop

---

## 1. WORKFLOW OVERVIEW

```
BURNING PROBLEM (User input or signal detection)
  ↓ [State: OBSERVE → CAPTURE]
PROBLEM DIAGNOSIS (D1 → D2 → D3)
  ↓ [State: CLASSIFY → CONNECT → RESEARCH → SYNTHESIZE]
HYPOTHESIS + IMPACT MATRIX
  ↓ [State: HYPOTHESIZE → CHALLENGE (RED TEAM)]
VALIDATED PROBLEM THESIS
  ↓ [State: PRIORITIZE]
CONTENT STRATEGY (C1) + PRODUCT HYPOTHESIS (P1)
  ↓ [State: DESIGN → SIMULATE]
SIMULATED SERIES ARCHITECTURE + PRODUCT MVP PLAN
  ↓ [State: PRODUCE → VERIFY (RED TEAM + QA)]
CONTENT OUTPUT (Script / Video / Series Plan)
  ↓ [State: PACKAGE → DISTRIBUTE]
PUBLISHED CONTENT (YouTube series launch)
  ↓ [State: MEASURE]
AUDIENCE DATA + CONTENT SIGNALS
  ↓ [State: DIAGNOSE → LEARN → STORE]
MEMORY UPDATED (Creative + Audience + Strategic)
  ↓ [State: REINVEST → RECONFIGURE]
PRODUCT FACTORY ACTIVATED (P1 → P2 → P4)
  ↓ [State: PRODUCE → VERIFY]
MVP BUILT + PRESOLD (Digital product / Tool / Course)
  ↓ [State: PACKAGE → DISTRIBUTE → MEASURE]
PRODUCT LAUNCHED + CUSTOMER DATA
  ↓ [State: DIAGNOSE → LEARN]
MEMORY UPDATED (Strategic + Operational + Failure)
  ↓ [State: REINVEST]
AGENTIC MVP (Agent-based tool / Automation / Intelligence layer)
  ↓ [State: PRODUCE → VERIFY → SCALE]
FULL ECOSYSTEM OPERATIONAL
  ↓ [State: SCALE / RECONFIGURE]
CONTINUOUSLY IMPROVING SYSTEM
```

---

## 2. DETAILED WORKFLOW STEPS WITH AGENT ASSIGNMENTS

### Phase A: Problem Detection and Diagnosis (States 01–07)

**Step 01 — OBSERVE (OMEGA-0, User)**
- Input: User describes burning problem, or Master Orchestrator detects signal from analytics / world memory
- Action: Create task ID. Build initial context packet with WORLD and AUDIENCE memory pins.
- Output: `task_id`, `problem_statement` (≤ 200 chars in packet thesis_statement)
- Memory: Read `WORLD` (related entities), `AUDIENCE` (behavior patterns), `FAILURE` (similar past failures)

**Step 02 — CAPTURE (OMEGA-0)**
- Input: Problem signal
- Action: Write `WORLD` entry (new signal detected) + `OPERATIONAL` entry (capture log)
- Output: `signal_id` in memory

**Step 03 — CLASSIFY (OMEGA-0)**
- Input: Captured signal
- Action: Route to Diagnosis Crew (D1 assigned). Build context packet with `STRATEGIC` pin (current thesis).
- Output: `diagnosis_task_id`

**Step 04 — CONNECT (OMEGA-D1)**
- Input: Problem + memory references
- Action: Read `STRATEGIC` (why this problem matters to thesis), `WORLD` (external context), `FAILURE` (similar failures)
- Output: `problem_layers` (symptom, structural, systemic, opportunity)

**Step 05 — RESEARCH (OMEGA-D1)**
- Input: Problem layers
- Action: Web search for evidence; read `WORLD` for competitor actions; read `AUDIENCE` for audience problem signals
- Output: `evidence_collection` (structured citations with URLs and confidence scores)

**Step 06 — SYNTHESIZE (OMEGA-D2)**
- Input: D1 diagnosis + evidence
- Action: Cross-examine D1 output. Identify alternative explanations. Propose contradiction tests.
- Memory: Read `FAILURE` (counter-evidence patterns)
- Output: `challenge_report`

**Step 07 — HYPOTHESIZE (OMEGA-D1)**
- Input: D1 diagnosis + D2 challenge + D3 impact matrix
- Action: Produce final diagnosis with confidence intervals, evidence requirements, risk analysis
- Memory: Write to `STRATEGIC` (new insight) + `FAILURE` (if new failure mode identified)
- Output: `validated_problem_thesis` → feeds both content and product paths

---

### Phase B: Content Strategy Design (States 08–11)

**Step 08 — CHALLENGE (OMEGA-C4)**
- Action: Red team reviews problem thesis for content relevance. Applies quality engine.
- Output: `red_team_review_content` (PUBLISH / REWORK / ABANDON recommendation)
- Memory: Write review to `OPERATIONAL` + `FAILURE` (if rejected)

**Step 09 — PRIORITIZE (OMEGA-C1)**
- Input: Validated problem thesis + impact matrix (D3)
- Action: Design content strategy: series architecture, format rules, emotional arc, monetization hook, editorial constitution
- Memory: Read `CREATIVE` (validated patterns), `AUDIENCE` (retention patterns for similar formats)
- Output: `content_strategy.json`

**Step 10 — DESIGN (OMEGA-C1 + OMEGA-C2)**
- Action: Design script structure with scene breakdown; define hook architecture; design retention curve
- Memory: Write design to `OPERATIONAL` + `CREATIVE` (new format proposal)
- Output: `script_blueprint.json`

**Step 11 — SIMULATE (OMEGA-C3 + OMEGA-C5)**
- Action: Predict retention curve; simulate channel graph propagation; design A/B test for hooks
- Memory: Read `AUDIENCE` (historical retention data), `CREATIVE` (hook patterns)
- Output: `simulation_report.json` + `channel_propagation_plan.json`

---

### Phase C: Content Production (States 12–15)

**Step 12 — PRODUCE (OMEGA-C2)**
- Input: Script blueprint + design + simulation
- Action: Generate script (structured by scene/shot/line). Apply anti-slop checks.
- Memory: Read `FAILURE` (past script failures) to avoid recurrence
- Output: `script.md` + `script.json`

**Step 13 — VERIFY (OMEGA-C4)**
- Action: Red team applies 5-score framework (C, T, P, B, R). Checks against No-AI-Slop Constitution.
- Output: `red_team_review.json` with recommendation
- Memory: Write review to `OPERATIONAL` + `FAILURE` (if quality failures found)
- Gate: Human approval required if `OMEGA_SCORE` < 0.6 or `RISK` > 0.3

**Step 14 — PACKAGE (OMEGA-E2 + OMEGA-E4)**
- Action: Package content with metadata (title, description, tags, thumbnail plan, analytics hooks, channel assignment)
- Memory: Write packaging spec to `OPERATIONAL`
- Output: `packaged_content/` directory + `analytics_config.json`

**Step 15 — DISTRIBUTE (OMEGA-E2)**
- Action: Deploy to selected channels (YouTube, podcast feed, community). Activate analytics tracking.
- Memory: Write distribution event to `AUDIENCE` + `OPERATIONAL`
- Output: `live_url` + `distribution_log.json`

---

### Phase D: Audience Intelligence and Memory Update (States 16–19)

**Step 16 — MEASURE (OMEGA-E4)**
- Action: Track audience behavior (views, retention, clicks, comments, conversions, search signals)
- Memory: Write `AUDIENCE` entries (behavior patterns, retention curves, comment clusters)
- Output: `measurement_report.json`

**Step 17 — DIAGNOSE (OMEGA-0 + OMEGA-D1)**
- Input: Measurement data + strategic memory
- Action: Analyze content performance against hypothesis. Identify what worked, what failed, why.
- Memory: Read `CREATIVE` (pattern match), `FAILURE` (if errors occurred), `WORLD` (external changes)
- Output: `performance_diagnosis.json`

**Step 18 — LEARN (OMEGA-M1)**
- Action: Synthesize insights. Propose improvements to content strategy, script format, hook design.
- Memory: Update `CREATIVE` (validated patterns), `STRATEGIC` (updated thesis if needed), `FAILURE` (if new failure discovered)
- Output: `insight_report.json` + `evolution_proposal.json` (optional)

**Step 19 — STORE (OMEGA-0)**
- Action: Archive all artifacts, memory updates, and state changes. Ensure rollback reference exists.
- Memory: Final sync across all banks. Update graph edges.
- Output: `archive_ref` + `rollback_reference`

---

### Phase E: Product Factory Activation (States 10–19, Parallel Path)

**Parallel Activation Trigger:** After `VALIDATED_PROBLEM_THESIS` produced in Step 07.

**Step P1 — PRODUCT ARCHITECT (OMEGA-P1)**
- Input: Problem thesis + content strategy (from Step 09) + audience signals
- Action: Design product hypothesis linking content signal to customer problem
- Memory: Read `AUDIENCE` (problem signals), `WORLD` (existing solutions), `STRATEGIC` (product thesis)
- Output: `product_hypothesis.json`

**Step P2 — CUSTOMER INTELLIGENCE (OMEGA-P4)**
- Action: Design interview protocol. Execute interviews (manual or automated surveys). Analyze responses.
- Memory: Write `AUDIENCE` (feedback summary) + `OPERATIONAL` (interview log)
- Output: `interview_analysis.json`

**Step P3 — SIMULATE / DESIGN (OMEGA-P1)**
- Input: Product hypothesis + interview analysis
- Action: Design MVP: feature set, value prop, price hypothesis, presell funnel, success metrics
- Memory: Read `CREATIVE` (format patterns for product presentation), `FAILURE` (failed products)
- Output: `mvp_plan.json`

**Step P4 — PRODUCE (OMEGA-P2)**
- Action: Build MVP using tech stack (Next.js + Stripe + database). Ensure analytics hooks.
- Memory: Write `OPERATIONAL` (deployment log) + `WORLD` (product fact)
- Output: `deployed_url` + `config.json`

**Step P5 — VERIFY (OMEGA-P3)**
- Action: Red team reviews product for economic value, feasibility, risk, audience trust.
- Memory: Write review to `OPERATIONAL` + `FAILURE` (if rejected)
- Gate: Human approval for launch if `OMEGA_SCORE` < 0.6

**Step P6 — PACKAGE / DISTRIBUTE (OMEGA-E2)**
- Action: Launch presell / MVP. Activate tracking. Connect to content funnel.
- Memory: Write `AUDIENCE` (conversion path) + `OPERATIONAL` (launch log)
- Output: `live_product_url` + `conversion_tracking_config.json`

**Step P7 — MEASURE / LEARN (OMEGA-P4 + OMEGA-M1)**
- Action: Analyze customer data. Update product hypothesis. Propose improvements.
- Memory: Update `STRATEGIC` (product thesis), `CREATIVE` (presentation patterns), `FAILURE` (if product errors)
- Output: `product_insight.json` + `next_version_proposal.json`

---

### Phase F: Agentic MVP Integration (States 20–22)

**Activation Condition:** After product achieves `MEASURE` with positive signal (conversion rate > baseline, retention > threshold).

**Step A1 — AGENTIC MVP ARCHITECT (OMEGA-P1 + OMEGA-0)**
- Input: Product data + content performance + audience behavior
- Action: Design agent-based layer that enhances product or creates new automation (e.g., AI assistant, content generator, analysis tool)
- Memory: Read all 6 banks for comprehensive context
- Output: `agentic_mvp_plan.json`

**Step A2 — PRODUCE / VERIFY / SCALE (OMEGA-P2 + OMEGA-M3)**
- Action: Build agentic layer using agent registry and state machine. Stress test. Verify. Scale if validated.
- Memory: Write `OPERATIONAL` (new agent config), `FAILURE` (test results)
- Output: `agentic_layer_url` + `scaling_plan.json`

---

## 3. WORKFLOW INTEGRATION POINTS

**Memory Integration Points:**
- Every step writes to at least one memory bank
- Every step reads from at least two memory banks (prevents isolation)
- Every red team step writes to `FAILURE` (even on success — records review process)
- Every measurement step writes to `AUDIENCE`
- Every strategic insight writes to `STRATEGIC`

**Agent Integration Points:**
- Master Orchestrator activates agents and manages context packets
- Each agent executes its contract and returns structured output
- Red team agents challenge before production continues
- Self-evolution agent monitors for improvement opportunities

**Human Integration Points:**
- Problem definition (user input required)
- Red team review execution (human approval for major outputs)
- Self-evolution approval (governance gate)
- Scale authorization (budget/resource gate)
- Strategic diagnosis review (human judgment for strategic shifts)

---

## 4. FAILURE HANDLING WITHIN WORKFLOW

Every phase includes failure paths:

```
PROBLEM → DIAGNOSIS FAILS (D2 challenge too strong, D1 reworks)
CONTENT → RED TEAM REJECTS (C4: ABANDON; C1: REWORK; C2: REWRITE)
PRODUCT → RED TEAM REJECTS (P3: ABANDON; P1: REVISE HYPOTHESIS)
CINEMA → QUALITY SCORE LOW (F3: CORRECT SHOT LIST; F4: RE-DIRECT)
DEPLOY → VERIFICATION FAILS (E2: ROLLBACK; FIX; RE-TEST)
```

Every failure triggers the failure-to-infrastructure loop:
```
FAILURE → WRITE FAILURE MEMORY → ROOT CAUSE → FIX → TEST → NEW GUARDRAIL → MEMORY UPDATE
```

---

## 5. WORKFLOW OBSERVABILITY

Every workflow execution produces:
- Complete context packet history
- Memory bank update log
- State machine transition log
- Agent execution log (with output contracts verified)
- Red team review results (with recommendations enforced)
- Analytics events (with tracking verified)
- Human gate approvals (with authorization references)

This creates a fully auditable, replayable, rollback-capable execution trail.
