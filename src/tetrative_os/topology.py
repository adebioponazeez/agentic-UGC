from __future__ import annotations

from .models import AgentSpec, Stage

WORKFLOW_VERSION = "220.0.0"


COMMON_GUARDRAIL = """
Separate facts, assumptions, and recommendations. Never invent evidence or claim tools were used when
not available. Seek disconfirming evidence. Prefer reversible steps. Flag legal, safety, privacy, IP,
and reputational risks. Output concise Markdown with explicit decisions and measurable next actions.
""".strip()


def agent(name: str, role: str, mandate: str, tools: tuple[str, ...] = ()) -> AgentSpec:
    return AgentSpec(
        name=name,
        role=role,
        tools=tools,
        system_prompt=f"You are {role}.\n{mandate}\n{COMMON_GUARDRAIL}",
    )


AGENTS: dict[str, AgentSpec] = {
    "diagnostician": agent("diagnostician", "a Gawdat-style profound-problem diagnostician", "Find the root mismatch between reality and expectations; distinguish symptoms, causes, incentives, and unknowns."),
    "researcher": agent("researcher", "an evidence and customer-research agent", "Build an evidence map, identify unknowns, and design cheap tests. Cite sources when research tools are attached.", ("web", "files")),
    "strategist": agent("strategist", "a venture and systems strategist", "Turn evidence into positioning, mechanisms, priorities, constraints, and kill criteria."),
    "creator": agent("creator", "a high-taste creative director and builder", "Create audience-native artifacts with strong hooks, specificity, emotional truth, and platform fit.", ("media",)),
    "operator": agent("operator", "an execution architect", "Convert decisions into owners, dependencies, interfaces, budgets, acceptance tests, and rollback plans.", ("code", "deploy")),
    "redteam": agent("redteam", "an adversarial red-team examiner", "Try to break the proposal. Test truth, demand, differentiation, ethics, security, feasibility, and second-order effects."),
    "evaluator": agent("evaluator", "an independent evaluation judge", "Score outputs against the rubric. Reject eloquence without evidence, executability, or measurable value."),
    "synthesizer": agent("synthesizer", "a chief synthesis officer", "Resolve contradictions without averaging away insight. Produce one coherent decision record and next action."),
}


WORKFLOWS: dict[str, tuple[Stage, ...]] = {
    "meta": (
        Stage("root_diagnosis", "diagnostician", "Diagnose the profound problem and define a falsifiable objective."),
        Stage("capability_map", "researcher", "Map required cognition, knowledge, tools, bottlenecks, and evidence gaps.", ("root_diagnosis",)),
        Stage("system_design", "strategist", "Design agents, protocols, memory, controls, metrics, and compounding loops.", ("root_diagnosis", "capability_map")),
        Stage("execution_plan", "operator", "Produce an implementation backlog with interfaces and acceptance tests.", ("system_design",), True),
        Stage("final_synthesis", "synthesizer", "Create the final decision record and immediate next actions.", ("execution_plan",)),
    ),
    "ugc": (
        Stage("audience_truth", "researcher", "Derive pains, desired identity, language, objections, and evidence gaps."),
        Stage("creative_strategy", "strategist", "Define content pillars, promise, formats, channel fit, and test matrix.", ("audience_truth",)),
        Stage("content_package", "creator", "Create hooks, script, shot list, caption, CTA, variants, and disclosure notes.", ("creative_strategy",)),
        Stage("production_plan", "operator", "Specify assets, generation pipeline, QC, publishing, tracking, and rollback.", ("content_package",), True),
        Stage("learning_brief", "synthesizer", "Define hypotheses, metrics, attribution limits, and next-iteration rules.", ("production_plan",)),
    ),
    "venture": (
        Stage("problem_market", "diagnostician", "Diagnose the painful job, current alternatives, buyer, and non-consumption."),
        Stage("evidence_map", "researcher", "Map market evidence, competitors, willingness-to-pay tests, and unknowns.", ("problem_market",)),
        Stage("venture_thesis", "strategist", "Specify wedge, mechanism, moat, business model, kill criteria, and 30-day bets.", ("evidence_map",)),
        Stage("product_and_gtm", "creator", "Create offer, landing-page narrative, outreach, demo story, and launch assets.", ("venture_thesis",)),
        Stage("operating_system", "operator", "Create delivery, sales, support, instrumentation, and deployment runbooks.", ("product_and_gtm",), True),
        Stage("board_memo", "synthesizer", "Synthesize decision, dissent, risks, capital allocation, and next gates.", ("operating_system",)),
    ),
    "outcome": (
        Stage("profound_diagnosis", "diagnostician", "Diagnose the expectation-reality gap, causal bottleneck, metric baseline, and falsifiable outcome."),
        Stage("epistemic_ledger", "researcher", "Separate observations, sourced evidence, assumptions, forecasts, contradictions, and unknowns.", ("profound_diagnosis",)),
        Stage("scenario_council", "strategist", "Model base, upside, downside, adversarial, and regime-change scenarios with leading indicators.", ("epistemic_ledger",)),
        Stage("option_portfolio", "strategist", "Create reversible strategic bets with impact, confidence, information value, owner, cost, and kill criteria.", ("scenario_council",)),
        Stage("capital_allocation", "operator", "Allocate capital, time, tools, and risk budgets across the option portfolio without violating guardrails.", ("option_portfolio",)),
        Stage("execution_campaign", "operator", "Build a 30-day traction campaign, 12-month compounding system, and 2030 option roadmap with approval and rollback.", ("capital_allocation",), True),
        Stage("feedback_control", "synthesizer", "Define observation cadence, trajectory thresholds, and amplify, continue, adapt, pivot, pause, or stop rules.", ("execution_campaign",)),
    ),
    "ecosystem": (
        Stage("root_diagnosis", "diagnostician", "Diagnose the ecosystem's profound problem, stakeholders, causes, and falsifiable outcomes."),
        Stage("intelligence_architecture", "researcher", "Map evidence, capabilities, models, tools, memory, unknowns, and evaluation requirements.", ("root_diagnosis",)),
        Stage("venture_engine", "strategist", "Design the venture portfolio, wedges, offers, economics, shared moats, experiments, and kill criteria.", ("root_diagnosis", "intelligence_architecture")),
        Stage("ugc_engine", "creator", "Design the audience-learning and UGC system: pillars, formats, production primitives, distribution tests, and trust controls.", ("venture_engine",)),
        Stage("agentic_operating_system", "operator", "Specify the integrated agent topology, interfaces, deployment, approvals, observability, security, and 90-day backlog.", ("intelligence_architecture", "venture_engine", "ugc_engine"), True),
        Stage("ecosystem_charter", "synthesizer", "Produce one charter containing decisions, preserved dissent, metrics, immediate actions, and evolution loops.", ("agentic_operating_system",)),
    ),
}
