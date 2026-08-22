from __future__ import annotations

import re
from dataclasses import dataclass

from .models import Candidate, Goal, Stage
from .providers import ModelProvider


@dataclass(slots=True)
class Score:
    total: float
    details: dict[str, float]
    critique: str


class Evaluator:
    """Hybrid deterministic checks + model cross-examination.

    Deterministic scoring keeps control flow reliable even when a judge model ignores formatting.
    The judge's critique provides semantic pressure while production deployments can replace this
    scorer with calibrated task-specific evals.
    """

    def __init__(self, provider: ModelProvider, evaluator_prompt: str, redteam_prompt: str) -> None:
        self.provider = provider
        self.evaluator_prompt = evaluator_prompt
        self.redteam_prompt = redteam_prompt

    def assess(self, goal: Goal, stage: Stage, candidate: Candidate) -> Score:
        content = candidate.content
        details = {
            "specificity": min(1.0, len(content) / 900),
            "structure": min(1.0, len(re.findall(r"^#{1,3} |^\d+\.", content, re.MULTILINE)) / 4),
            "executability": 1.0 if re.search(r"metric|test|next|execute|validate", content, re.I) else 0.35,
            "risk_awareness": 1.0 if re.search(r"risk|unknown|assumption|failure", content, re.I) else 0.25,
        }
        total = sum(details.values()) / len(details)
        critique = self.provider.generate(
            self.redteam_prompt,
            f"GOAL: {goal.objective}\nSTAGE: {stage.name}\nCANDIDATE:\n{content}\n\n"
            "Cross-examine this. Name the strongest failure mode, unsupported assumption, ethical risk, "
            "and one decisive falsification test.",
            temperature=0.0,
        )
        judge = self.provider.generate(
            self.evaluator_prompt,
            f"Evaluate this {stage.name} output for truthfulness, relevance, novelty, execution readiness, "
            f"and risk control. Deterministic score is {total:.2f}. Explain what must improve:\n{content}",
            temperature=0.0,
        )
        return Score(total, details, f"{critique}\n\n### Judge\n{judge}")
