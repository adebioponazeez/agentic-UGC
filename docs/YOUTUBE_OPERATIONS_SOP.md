# OMEGA YOUTUBE OPERATIONS SOP v1.0
## Integration of Advanced Tools → Top of Funnel → Real Metrics → Scale Production
## Based on reverse-engineered architectures of 20–500M subscriber ecosystems

---

## 1. THE THESIS (NOT A PROMPT)

Conventional YouTube SOPs optimize for outputs (videos, thumbnails, tags).  
OMEGA YouTube Operations optimizes for **learning velocity × audience trust × institutional memory**.

The real metric is not views. It is **durable value per unit of attention, capital, and compute**.

Every video must be:
- A **controlled experiment** (hypothesis → content → audience response → data → insight → memory → better hypothesis)
- A **signal generator** (not noise — validated by retention, sentiment, search signal, conversion)
- A **memory contributor** (feeds Creative, Audience, Strategic, World, Failure banks)
- A **funnel component** (connects to product factory, membership, enterprise studio)

---

## 2. TOOL ARCHITECTURE (EXECUTABLE, NOT ASPIRATIONAL)

### 2.1 SGNL (Signal, Not Generic — Custom Signal Framework)
**Concept:** Every piece of content is evaluated as signal or noise before publication.

**Signal Criteria (must pass ≥ 3 of 5):**
1. **Retention Signal:** Retention curve predicts ≥ 50% at 30 seconds (validated by Audience Memory patterns)
2. **Sentiment Signal:** Positive sentiment ratio ≥ 0.75 (from comment clustering + NLP)
3. **Search Signal:** Search volume for core topic increases within 7 days of publication (measured via analytics + external trends)
4. **Propagation Signal:** Channel Graph Operator predicts successful transformation to Long-Form or Product (C5 routing approved)
5. **Conversion Signal:** Click-through to product/member/community exceeds baseline for format

**Noise Criteria (any one = abandon/rework):**
- Generic format (no originality claim verified by red team)
- Synthetic emotional manipulation (no emotional arc with documented progression)
- Missing evidence citations (truth score < 0.8)
- No transformation claim (viewer gains nothing new)
- Context pollution score > 0.3 or failure memory pin missing

**Implementation:** `core/youtube/signal_filter.py` — automated filtering with memory integration.

---

### 2.2 TubeBuddy Integration Framework
**Purpose:** Keyword research, SEO optimization, A/B testing infrastructure, competitive analysis.

**Integration Design:**
```yaml
agent_integration:
  agent: OMEGA-Y1  # YouTube Operations Agent
  tool_interface: tube_buddy_proxy
  data_sources:
    - keyword_explorer: "search_volume, competition_score, optimization_strength"
    - tag_explorer: "tag_rankings, related_tags, video_tags"
    - competitor_tracker: "channel_metrics, video_performance, upload_frequency"
    - ab_testing: "thumbnail_variants, title_variants, description_variants"
  memory_integration:
    - write: CREATIVE (format patterns), WORLD (keyword entities), AUDIENCE (search behavior)
    - read: FAILURE (past SEO errors), STRATEGIC (current keyword thesis)
  output_contract: seo_strategy.json
  failure_conditions: "No memory updates = abort; no red team review for major SEO strategy = abort"
```

**Real Metric Target:**
- Keyword optimization strength ≥ 80% (TubeBuddy metric equivalent)
- Search-driven traffic ≥ 30% of total views within 30 days
- Competitor analysis feeds strategic thesis (not just imitation)

---

### 2.3 vidIQ Integration Framework
**Purpose:** Channel analytics, competitor intelligence, trend forecasting, content performance benchmarking.

**Integration Design:**
```yaml
agent_integration:
  agent: OMEGA-Y1 / OMEGA-E1  # Operations + Ecosystem
  tool_interface: vid_iq_proxy
  data_sources:
    - channel_analytics: "subscriber_growth, view_velocity, engagement_rate, earnings_estimate"
    - competitor_analysis: "top_videos, upload_schedule, growth_rate, content_themes"
    - trend_alerts: "emerging_topics, trending_formats, audience_shift_signals"
    - video_scoring: "video_performance_index, optimization_score, engagement_depth"
  reverse_engineering_protocol:
    - select_competitors: "channels with 20M–500M subscribers in relevant vertical"
    - extract_structures: "format patterns, emotional arcs, evidence approaches, monetization hooks"
    - compare_memory: "match competitor patterns against CREATIVE MEMORY (validated / rejected)"
    - design_derivative: "transform (not duplicate) competitor insight into original series architecture"
    - enforce_identity: "red team must confirm identity claim (not cloned strategy)"
  output_contract: competitor_intelligence_report.json + derivative_series_plan.json
```

**Reverse Engineering Protocol (Non-Negotiable):**
Every competitor insight must pass through:
1. **Extraction:** What does this top channel do structurally? (Not what they say — what they execute)
2. **Validation:** Does this match any validated pattern in our Creative Memory? (If yes: reference; if no: treat as new experiment)
3. **Transformation:** How is our output different? (Format, depth, identity, evidence, emotional architecture must differ)
4. **Guardrail:** Does this violate No-AI-Slop Constitution? (Generic format = automatic rejection)
5. **Memory Update:** Every reverse-engineered insight writes to Creative Memory (validated/rejected) and Strategic Memory (competitive thesis update)

---

### 2.4 Social Blade Integration Framework
**Purpose:** Channel performance tracking, earnings estimation, subscriber velocity, upload frequency analysis, growth trajectory modeling.

**Integration Design:**
```yaml
agent_integration:
  agent: OMEGA-E4  # Analytics Architect + OMEGA-M1 (Self-Evolution)
  tool_interface: social_blade_proxy
  data_sources:
    - subscriber_velocity: "daily_growth, monthly_growth, yearly_trajectory"
    - view_velocity: "daily_views, monthly_views, peak_identification"
    - earnings_estimate: "monthly_range, yearly_range, cpm_indicators"
    - upload_frequency: "videos_per_week, consistency_score, schedule_patterns"
    - grade_metrics: "channel_grade, subscriber_rank, video_view_rank"
  analytics_integration:
    - write: AUDIENCE (behavior patterns), OPERATIONAL (performance logs)
    - update_memory: "Every 7 days — aggregate Social Blade data; write to audience behavior patterns"
  scale_decision_support:
    - trigger_scale_analysis: "When subscriber_velocity exceeds 2x baseline for 14 consecutive days"
    - trigger_retirement_analysis: "When view_velocity declines for 30 consecutive days with no successful experiments"
```

---

### 2.5 Additional Tool Integration (Modular Design)

**Google Trends / Search Console:**
- Integrated via `analytics/SCHEMA.md` event tracking
- Search signal events (`search_signal`) write to `WORLD_MEMORY` (trend entities) and `AUDIENCE_MEMORY` (search behavior patterns)

**YouTube Analytics API:**
- Direct event source for `content_view`, `content_retention`, `content_click`, `conversion` events
- Every event writes to appropriate memory bank automatically
- Analytics dashboard (`deployment/docker-compose.yml` Grafana instance) displays aggregated metrics

**Whisper / Audio Analysis:**
- Used in cinematic pipeline (`OMEGA-F5`) for sound design verification
- Audio retention curves integrated into `CREATIVE_MEMORY`

**Runway / Pika / Stable Video Diffusion:**
- AI generation tools integrated in `CINEMA_DIVISION`
- Every generation parameter set writes to `CREATIVE_MEMORY` (visual grammar patterns)
- Anti-slop verification (`intention`, `information`, `emotion`, `identity`, `transformation`) enforced before output approval

---

## 3. REVERSE ENGINEERING FRAMEWORK: TOP CHANNEL SYSTEMS (20–500M SUBSCRIBERS)

### 3.1 Selection Criteria for Reverse Engineering

Not every large channel is worth studying. The framework selects competitors based on:

```
SELECTION ALGORITHM:
1. SUBSCRIBER RANGE: 20M ≤ subscribers ≤ 500M (proven scale, not just viral anomaly)
2. VERTICAL ALIGNMENT: Shares at least 2 of 4 dimensions with our strategic thesis
   - Topic domain (documentary, business, technology, culture, science, etc.)
   - Audience segment (entrepreneurs, creators, filmmakers, architects, etc.)
   - Format approach (faceless, interview, cinematic essay, investigative, etc.)
   - Monetization model (ads, products, membership, enterprise, licensing)
3. PERFORMANCE VALIDITY: Subscriber velocity ≥ baseline; retention patterns consistent; upload frequency stable
4. CREATIVE ORIGINALITY: Has identifiable authored identity (not generic AI output)
5. EVIDENCE INTEGRITY: Source citations visible; claims verifiable; no fabricated evidence
```

**Output:** `core/youtube/reverse_engineering/competitor_selection.json` — structured selection report for red team review before any reverse engineering begins.

---

### 3.2 Structural Extraction Protocol

Once selected, every competitor is analyzed across 14 dimensions (matching our Cinema Division departments):

```
DIMENSION 1 — STORY DEVELOPMENT (F1):
- Premise clarity (1 sentence test)
- Theme depth (number of layers explored)
- Emotional arc design (documented progression)
- World rules (consistency, constraints, reality framework)
- Series architecture (cumulative thesis vs. standalone videos)

DIMENSION 2 — SCREENWRITING (F2):
- Scene structure (acts, chapters, sequences)
- Dialogue / narration style (authored vs. generic)
- Evidence integration (how claims are supported)
- Hook design (opening 60 seconds structure)
- Transformation claim (what viewer gains)

DIMENSION 3 — DIRECTING (F4):
- Emotional progression tracking (per scene targets)
- Performance direction (voice, character, presentation)
- Pacing design (retention curve alignment)
- Audience relationship (direct address vs. observation vs. immersion)

DIMENSION 4 — CINEMATOGRAPHY (F3):
- Shot design (intention per shot documented?)
- Visual identity (color, texture, light, framing philosophy)
- Camera movement (meaningful vs. decorative)
- AI generation parameters (if applicable — what capabilities added?)
- Visual evidence presentation (data, footage, documentation)

DIMENSION 5 — CHARACTER SYSTEMS (F5 / extended):
- Character identity (if present — real, synthetic, representative?)
- Voice/authorship (specific perspective vs. universal claim)
- Audience identification mechanism

DIMENSION 6 — WORLD BUILDING (F6 / extended):
- Reality framework (documentary truth vs. speculative vs. educational)
- Visual consistency (world rules maintained across videos)
- Evidence framework (sources, citations, verification methods)

DIMENSION 7 — EDITING / SOUND / FINISHING (F5 core):
- Editing decision structure (what is kept, what is cut, why?)
- Sound design (audio emotional progression)
- Color grading (visual identity consistency)
- Final output format (vertical, horizontal, episode length)
- Retention analysis (where does attention collapse?)

DIMENSION 8 — DISTRIBUTION / CHANNEL GRAPH (E1 / E5):
- Channel architecture (how videos connect to series)
- Propagation strategy (short → long-form → documentary → product)
- Audience journey design (content → community → product → enterprise)
- Monetization integration (explicit link, not decorative)

DIMENSIONS 9–14 — ADDITIONAL SYSTEM ANALYSIS:
- Memory integration (does competitor accumulate institutional knowledge?)
- Self-evolution (does their system improve over time? How is evidence used?)
- Governance / quality control (red team equivalent? Quality framework?)
- Automation level (manual, assisted, workflow, agentic, adaptive?)
- Portfolio intelligence (multi-channel coordination or independent operation?)
- Enterprise integration (B2B media infrastructure present?)
```

Every dimension produces a structured entry in `core/youtube/reverse_engineering/competitor_[id].json`.  
Every entry must include: `original_observation`, `evidence_reference` (video URL + timestamp), `memory_reference` (CREATIVE / STRATEGIC / FAILURE bank entries), `transformation_plan` (how our system will adapt — not copy — this insight), `red_team_review_status`.

---

### 3.3 The Anti-Cloning Enforcement (Governance Level)

Every reverse-engineering result must pass through `OMEGA-M4` (Governance Guardian) checks:

```
ANTI-CLONING CHECKS:
1. IDENTITY CLAIM: Does our proposed output express a different authored perspective?
2. FORMAT DIFFERENCE: Does our output change format, structure, or visual approach?
3. DEPTH DIFFERENCE: Does our output add evidence, analysis, or perspective not present in competitor?
4. EMOTIONAL DIFFERENCE: Does our emotional arc serve a different audience need?
5. EVIDENCE DIFFERENCE: Does our evidence framework use different sources or verification methods?
6. MEMORY INTEGRATION: Does our output contribute new patterns to institutional memory (not just replicate)?
7. STRATEGIC ALIGNMENT: Does this serve our strategic thesis (not competitor's thesis)?

FAILURE: Any check fails = proposal rejected; competitor insight archived in CREATIVE MEMORY as "rejected pattern" with reasoning; new experiment proposed within 48 hours.
```

---

## 4. SIGNAL-TO-NOISE PLAYBOOK (VERY HIGH SIGNAL — VERY LOW NOISE)

### 4.1 The SGNL Filter Engine (`core/youtube/signal_filter.py`)

Every content proposal and every competitor insight passes through:

```python
class SignalNoiseFilter:
    """SGNL (Signal Not Generic / Noise Eliminated) framework."""

    SIGNAL_DIMENSIONS = ["retention", "sentiment", "search", "propagation", "conversion"]
    NOISE_TRIGGERS = ["generic_format", "synthetic_emotion", "missing_evidence",
                      "no_transformation", "pollution_high", "failure_pin_missing",
                      "thesis_misalign", "red_team_unresolved"]

    def evaluate_content_proposal(self, proposal: Dict) -> Dict:
        """Returns: signal_score [0-1], noise_flags [list], recommendation [string]."""
        signal_score = 0.0
        noise_flags = []

        # Signal checks
        if proposal.get("predicted_retention_30s", 0) >= 0.50:
            signal_score += 0.20
        else:
            noise_flags.append("low_retention_prediction")

        if proposal.get("positive_sentiment_prediction", 0) >= 0.75:
            signal_score += 0.20
        else:
            noise_flags.append("low_sentiment_prediction")

        if proposal.get("search_signal_present", False):
            signal_score += 0.20
        else:
            noise_flags.append("missing_search_signal")

        if proposal.get("propagation_approved", False):
            signal_score += 0.20
        else:
            noise_flags.append("propagation_not_approved")

        if proposal.get("conversion_link_valid", False):
            signal_score += 0.20
        else:
            noise_flags.append("conversion_link_invalid")

        # Noise checks (hard elimination)
        if proposal.get("originality_claim_verified", False) is False:
            noise_flags.append("generic_format_unverified")

        if proposal.get("anti_slop_check_passed", False) is False:
            noise_flags.append("anti_slop_check_failed")

        if proposal.get("context_pollution_score", 1.0) > 0.3:
            noise_flags.append("pollution_too_high")

        if proposal.get("red_team_review_complete", False) is False:
            noise_flags.append("red_team_unresolved")

        # Recommendation
        if len(noise_flags) > 0:
            recommendation = "ABANDON" if len(noise_flags) >= 2 else "REWORK"
        else:
            recommendation = "PUBLISH" if signal_score >= 0.6 else "REWORK"

        if signal_score >= 0.8 and len(noise_flags) == 0:
            recommendation = "SCALE_FAST"

        return {
            "signal_score": signal_score,
            "noise_flags": noise_flags,
            "recommendation": recommendation,
            "signal_dimensions_met": [d for d in self.SIGNAL_DIMENSIONS
                                       if d not in [f.replace("low_", "").replace("missing_", "").replace("unverified", "")
                                                 for f in noise_flags if d in f]],
            "proposal_ref": proposal.get("proposal_id"),
            "red_team_required": recommendation in ["REWORK", "ABANDON", "SCALE_FAST"],
        }
```

---

### 4.2 The High-Signal Production Protocol

Every piece of content produced through OMEGA YouTube Operations must follow this exact sequence:

```
1. HYPOTHESIS FORMATION (OMEGA-C1 + OMEGA-D1)
   → Problem thesis + content strategy + editorial constitution

2. SIGNAL PREDICTION (OMEGA-Y1 + SGNL Filter)
   → Retention prediction, sentiment prediction, search signal check, propagation check, conversion check
   → Output: signal_score, noise_flags, recommendation

3. RED TEAM REVIEW (OMEGA-C4 + OMEGA-M2)
   → If recommendation = SCALE_FAST: full council review (10 critics)
   → If recommendation = PUBLISH: critical path review (creative, truth, cinematic, retention, business)
   → If recommendation = REWORK / ABANDON: return to step 1 or archive in FAILURE MEMORY

4. CONTENT PRODUCTION (OMEGA-C2 / F2 / F3 / F4 / F5)
   → Script, cinematography plan, direction notes, finishing plan
   → Every step writes to CREATIVE MEMORY (format patterns, visual grammar, emotional arcs)

5. QUALITY ENGINE VERIFICATION (OMEGA-0 / M4)
   → 5 scores: C, T, P, B, R
   → OMEGA SCORE calculation
   → Gate enforcement: PUBLISH requires score > 0.6 + R < 0.3 + red team complete

6. PACKAGING + ANALYTICS HOOKS (OMEGA-E2 + E4)
   → Metadata (title, description, tags, thumbnail plan)
   → Analytics tracking (event definitions, dimension setup)
   → Memory pin configuration (which banks updated by this output)

7. DISTRIBUTION (OMEGA-E2)
   → Channel graph assignment (which channels in 60-channel topology)
   → Propagation plan (if validated signal, design transformed outputs for other nodes)
   → Launch with tracking active

8. MEASUREMENT (OMEGA-E4 + Analytics Module)
   → Real-time tracking: retention curve, watch time, click-through, sentiment, search signal, conversion
   → Every event writes to appropriate memory bank

9. DIAGNOSIS + LEARNING (OMEGA-M1 + D1)
   → Performance vs. hypothesis comparison
   → Insight extraction (what worked, what failed, why)
   → Memory updates: CREATIVE (validated/rejected patterns), AUDIENCE (behavior updates), STRATEGIC (thesis adjustments), FAILURE (if errors occurred)

10. SELF-EVOLUTION PROPOSAL (OMEGA-M1)
    → If performance exceeds threshold: propose scale (resource increase, new series, new format)
    → If performance below threshold: propose rework or abandonment (with evidence)
    → If new failure mode detected: write FAILURE MEMORY; propose new guardrail

11. RECONFIGURE / SCALE / ABANDON (OMEGA-0 + M4 + M1)
    → Governance approval required for structural changes
    → Human gate confirmation for scale authorization
    → Rollback mechanism activated for any failure
```

---

## 5. SCALE PRODUCTION PROTOCOL

### 5.1 Scale Triggers (Automatic Analysis — Requires Human Gate)

```
TRIGGER CONDITIONS (any 2 of 4 in 14-day window):
1. SUBSCRIBER VELOCITY: Daily growth rate > 2x 90-day baseline for 14 consecutive days
2. RETENTION IMPROVEMENT: Average retention at 30s increases by > 10% over previous 30-day average
3. CONVERSION IMPROVEMENT: Product/community/member conversion rate increases by > 20% over baseline
4. PROPAGATION SUCCESS: At least 1 validated signal successfully propagated through channel graph with positive performance

AUTOMATIC ACTIONS (no human gate required for observation):
- Write strategic memory entry (scale signal detected)
- Update audience memory (behavior shift observed)
- Update operational memory (performance metrics logged)
- Trigger self-evolution proposal generation (OMEGA-M1 activates)

HUMAN GATE REQUIRED (before any resource reallocation):
- Budget increase > 20% of current portfolio allocation
- New agent activation for expanded production
- New channel creation in 60-channel topology
- Enterprise studio proposal for scaled media system
```

---

### 5.2 Scale Execution (After Gate Approval)

```
PHASE 1 — RESOURCE REALLOCATION (OMEGA-E1 + M1):
- Identify underperforming channels/experiments for retirement
- Identify validated signals for promotion
- Propose resource shift: production hours, agent activation frequency, budget percentage
- Red team review for portfolio-level decision

PHASE 2 — PRODUCTION EXPANSION (OMEGA-0 + C1 + P1):
- Design expanded series architecture (more episodes, deeper exploration, new formats)
- Design expanded product architecture (new features, new tiers, new delivery models)
- Ensure memory integration continues (expanded output = expanded learning events)

PHASE 3 — AUTOMATION INCREASE (OMEGA-M1 + E2):
- Evaluate which workflow phases can be automated further (Level 3 → Level 4 → Level 5)
- Propose agent collaboration patterns (multi-agent execution with shared context)
- Implement automation improvements with rollback capability

PHASE 4 — OBSERVATION + LEARNING (OMEGA-M1 + D1 + E4):
- Monitor scaled output performance against expanded hypothesis
- Update all memory banks with new patterns
- Propose next evolution (compound improvement)
```

---

## 6. IMPLEMENTATION FILES (ACTUALLY EXECUTABLE)

### 6.1 Agent Addition: `core/youtube/agent_y1.py`
**OMEGA-Y1 — YouTube Operations Agent**

Contracts:
- `ROLE`: Execute YouTube operations — tool integration, signal filtering, reverse engineering, scale analysis, analytics integration
- `TASK`: Manage content pipeline metrics; execute SGNL filtering; reverse engineer competitor structures; propose scale/rework/abandon; integrate analytics events with memory
- `AVAILABLE_TOOLS`: `youtube_tool_proxy`, `signal_filter_engine`, `reverse_engineer_framework`, `analytics_event_recorder`, `memory_read_write`, `red_team_scheduler`
- `RELEVANT_KNOWLEDGE`: `CREATIVE` (format patterns), `AUDIENCE` (behavior patterns), `WORLD` (trend entities), `FAILURE` (past errors), `OPERATIONAL` (deployment/state logs)
- `OUTPUT_CONTRACT`: Structured JSON with `signal_analysis`, `competitor_insight`, `scale_recommendation`, `analytics_events`, `memory_updates`
- `FAILURE_CONDITIONS`: No SGNL filter execution = abort; no memory updates = abort; no red team review for major recommendations = abort; reverse engineering without identity claim = abort

### 6.2 Signal Filter Engine: `core/youtube/signal_filter.py`
As shown in Section 4.1 — executable Python class with evaluation logic.

### 6.3 Reverse Engineering Framework: `core/youtube/reverse_engineering/`
Directory structure:
```
core/youtube/reverse_engineering/
├── framework.md              # Protocol specification (Section 3)
├── competitor_selection.py   # Algorithm implementation (Section 3.1)
├── structural_extraction.py  # 14-dimension analysis (Section 3.2)
├── anti_cloning_guardian.py  # Governance enforcement (Section 3.3)
├── competitor_[channel].json # Example output format
└── memory_integration.py     # How reverse-engineered insights feed Creative/Strategic/Failure memory
```

### 6.4 Analytics Integration Update: `analytics/youtube/SOP.md`
Detailed event schema extensions for YouTube-specific metrics:
- `youtube_video_published`
- `youtube_retention_curve`
- `youtube_search_signal`
- `youtube_competitor_insight`
- `youtube_scale_trigger`
- `youtube_abandon_event`

### 6.5 Deployment Update: `deployment/docker-compose.yml`
Add YouTube operations services:
```yaml
  youtube-analytics-collector:
    image: python:3.12-slim
    container_name: omega-youtube-analytics
    volumes:
      - ./core/youtube:/app/youtube
      - ./analytics/youtube:/app/analytics/youtube
    networks:
      - omega-net
    command: ["python", "-m", "youtube.analytics_collector"]
```

---

## 7. METRICS THAT MATTER (NOT VANITY)

Every metric tracked through this SOP connects to institutional memory and strategic decision-making:

```
CONTENT METRICS (Memory Integration):
- retention_30s / retention_60s / retention_full → Creative Memory (format validation)
- watch_time_total / watch_time_average → Audience Memory (behavior patterns)
- positive_sentiment_rate → Audience Memory (sentiment patterns) + Creative Memory (hook validation)
- click_through_rate → Strategic Memory (monetization effectiveness)
- conversion_rate → Strategic Memory (product-market fit) + Audience Memory (conversion paths)
- search_signal_strength → World Memory (trend entities) + Audience Memory (search behavior)

COMPETITOR METRICS (Reverse Engineering Integration):
- competitor_subscriber_range → Operational Memory (competitive landscape)
- competitor_format_similarity → Creative Memory (validated / rejected patterns)
- competitor_evidence_approach → Creative Memory (evidence framework patterns)
- competitor_emotional_arc → Creative Memory (emotional progression patterns)
- competitor_monetization_model → Strategic Memory (business thesis updates)

SCALE METRICS (Self-Evolution Integration):
- subscriber_velocity_change → Strategic Memory (growth signals)
- retention_trend_change → Creative Memory (format improvement evidence)
- conversion_trend_change → Strategic Memory (business model validation)
- memory_growth_rate → Operational Memory (institutional intelligence accumulation)
- learning_velocity → Strategic Memory (system capability improvement rate)
```

---

## 8. NON-NEGOTIABLE RULES (YOUTUBE-SPECIFIC ADDITIONS TO OMEGA CONSTITUTION)

1. **Every video is an experiment.** No exceptions. No decorative uploads. Every output must have a testable hypothesis, a measurement plan, and a memory update protocol.

2. **Every competitor insight is transformed, not duplicated.** The anti-cloning guard ensures identity claim, format difference, depth difference, emotional difference, evidence difference, and strategic alignment before any reverse-engineered insight is integrated.

3. **Signal must exceed noise by ≥ 3 dimensions.** The SGNL filter requires at least 3 of 5 signal dimensions (retention, sentiment, search, propagation, conversion) to pass. Any noise trigger (generic format, synthetic emotion, missing evidence, no transformation, pollution high, failure pin missing, thesis misalignment, red team unresolved) requires rework or abandonment.

4. **Analytics events feed memory automatically.** Every `youtube_video_published`, `youtube_retention_curve`, `youtube_search_signal`, and `youtube_scale_trigger` event writes to the appropriate memory bank. No event = no memory update = no institutional learning.

5. **Scale requires evidence + approval.** Automatic observation of scale triggers is permitted (memory updates, proposal generation). Actual resource reallocation requires human gate confirmation, red team review, and governance guardian approval.

6. **Failure memory is permanent and non-deletable.** Every error (low retention, synthetic output detected, evidence missing, anti-slop failure, governance violation, scale failure) generates a structured FAILURE MEMORY entry: `Failure → Cause → Fix → Test → New Guardrail`.

7. **Quality engine scores are non-decorative.** Every major content output, every competitor insight, every scale proposal receives the 5-score framework (`C × T × P × B × (1 - R)`). Scores below thresholds trigger enforced actions (REWORK / ABANDON). Scores above thresholds with low risk trigger SCALE FAST — but only after full red team review.

---

## 9. NEXT IMPLEMENTATION PROTOCOL

**Phase 1 (Days 1–3 of YouTube Operations):**
- Implement `OMEGA-Y1` agent with tool interfaces (`youtube_tool_proxy` with SGNL filter)
- Configure analytics event schema extensions (`analytics/youtube/SOP.md`)
- Initialize competitor selection algorithm (`core/youtube/reverse_engineering/competitor_selection.py`)
- Run first SGNL filter test on proposed content strategy
- Write first FAILURE MEMORY entry for YouTube operations (even on success — establish protocol)

**Phase 2 (Days 4–7):**
- Execute reverse engineering of 3–5 selected competitors (20M–500M range)
- Generate structured competitor reports with transformation plans
- Execute red team review on all competitor-derived proposals
- Integrate validated competitor insights into Creative Memory
- Design first expanded series architecture based on validated patterns

**Phase 3 (Days 8–10):**
- Launch first content through full pipeline (hypothesis → SGNL filter → red team → production → quality verification → distribution → measurement → memory → evolution proposal)
- Verify analytics tracking works end-to-end (event → memory → dashboard)
- Verify signal filtering prevents noise publication (test with low-quality proposal — must trigger ABANDON/REWORK)
- Verify scale trigger detection works (simulate high-performance signal — must trigger proposal without automatic resource allocation)
- Write final governance audit (M4 verification of all rules enforced)
