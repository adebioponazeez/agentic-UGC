from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from math import isfinite
from typing import Any
from uuid import uuid4


class Direction(str, Enum):
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"


class OutcomeStatus(str, Enum):
    ACTIVE = "active"
    AHEAD = "ahead"
    ON_TRACK = "on_track"
    BEHIND = "behind"
    CRITICAL = "critical"
    PAUSED = "paused"
    ACHIEVED = "achieved"
    STOPPED = "stopped"


class RecalibrationMode(str, Enum):
    AMPLIFY = "amplify"
    CONTINUE = "continue"
    ADAPT = "adapt"
    PIVOT_OR_STOP = "pivot_or_stop"
    ACHIEVED = "achieved"


@dataclass(slots=True)
class Metric:
    name: str
    unit: str
    baseline: float
    target: float
    direction: Direction = Direction.MAXIMIZE

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        self.unit = self.unit.strip()
        if not self.name or not self.unit:
            raise ValueError("Metric name and unit are required")
        if not isfinite(self.baseline) or not isfinite(self.target):
            raise ValueError("Metric baseline and target must be finite")
        if self.baseline == self.target:
            raise ValueError("Metric target must differ from baseline")
        if self.direction is Direction.MAXIMIZE and self.target < self.baseline:
            raise ValueError("A maximize target must exceed its baseline")
        if self.direction is Direction.MINIMIZE and self.target > self.baseline:
            raise ValueError("A minimize target must be below its baseline")

    def progress(self, value: float) -> float:
        distance = self.target - self.baseline
        return (value - self.baseline) / distance

    def value_at_progress(self, progress: float) -> float:
        return self.baseline + ((self.target - self.baseline) * progress)


@dataclass(slots=True)
class StrategicBet:
    title: str
    owner: str
    hypothesis: str
    expected_impact: float
    confidence: float
    requested_cost_minor: int
    reversible: bool
    kill_criterion: str
    evidence: list[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        for name in ("title", "owner", "hypothesis", "kill_criterion"):
            if not getattr(self, name).strip():
                raise ValueError(f"Bet {name} is required")
        if not isfinite(self.expected_impact) or not isfinite(self.confidence):
            raise ValueError("Bet impact and confidence must be finite")
        if not 0 <= self.expected_impact <= 1 or not 0 <= self.confidence <= 1:
            raise ValueError("Bet impact and confidence must be between zero and one")
        if self.requested_cost_minor < 0:
            raise ValueError("Bet cost cannot be negative")

    @property
    def strategic_score(self) -> float:
        reversibility = 1.25 if self.reversible else 0.7
        information_value = 1 + ((1 - self.confidence) * 0.35)
        cost_penalty = 1 + (self.requested_cost_minor / 100_000)
        return round(
            (self.expected_impact * self.confidence * reversibility * information_value) / cost_penalty,
            6,
        )


@dataclass(slots=True)
class AuthorityEnvelope:
    allowed_tools: list[str] = field(default_factory=list)
    max_risk: str = "low"
    total_spend_minor: int = 0
    approval_spend_threshold_minor: int = 0
    max_actions_per_day: int = 20
    protected_categories: list[str] = field(
        default_factory=lambda: [
            "payment",
            "publish",
            "identity",
            "external_message",
            "delete",
            "contract",
            "credential",
            "production_deploy",
        ]
    )
    kill_switch: bool = False

    def __post_init__(self) -> None:
        self.allowed_tools = [tool.strip().lower() for tool in self.allowed_tools if tool.strip()]
        self.protected_categories = [
            category.strip().lower() for category in self.protected_categories if category.strip()
        ]
        if self.max_risk not in {"low", "medium", "high", "critical"}:
            raise ValueError("Invalid authority risk ceiling")
        if self.total_spend_minor < 0 or self.approval_spend_threshold_minor < 0:
            raise ValueError("Authority spend values cannot be negative")
        if self.max_actions_per_day < 1:
            raise ValueError("Authority must allow at least one action per day")


@dataclass(slots=True)
class StrategicOutcome:
    title: str
    north_star: str
    owner: str
    metric: Metric
    capital_budget_minor: int
    guardrails: list[str]
    bets: list[StrategicBet]
    authority: AuthorityEnvelope
    deadline_days: int = 1460
    id: str = field(default_factory=lambda: str(uuid4()))
    schema_version: int = 220
    status: OutcomeStatus = OutcomeStatus.ACTIVE
    paused_from_status: OutcomeStatus | None = None
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def __post_init__(self) -> None:
        if not self.title.strip() or not self.north_star.strip() or not self.owner.strip():
            raise ValueError("Outcome title, north star, and owner are required")
        if self.capital_budget_minor < 0:
            raise ValueError("Capital budget cannot be negative")
        if not 1 <= self.deadline_days <= 3650:
            raise ValueError("Outcome deadline must be between one day and ten years")
        if not self.guardrails:
            raise ValueError("At least one outcome guardrail is required")
        if not self.bets:
            raise ValueError("At least one strategic bet is required")
        if self.authority.total_spend_minor > self.capital_budget_minor:
            raise ValueError("Autonomous spend envelope cannot exceed the outcome capital budget")


@dataclass(slots=True)
class HorizonMilestone:
    days: int
    target_value: float
    target_progress: float
    intent: str


@dataclass(slots=True)
class BetAllocation:
    bet_id: str
    title: str
    strategic_score: float
    allocated_minor: int
    rationale: str


@dataclass(slots=True)
class StrategicPlan:
    outcome_id: str
    horizons: list[HorizonMilestone]
    allocations: list[BetAllocation]
    unallocated_minor: int
    generated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass(slots=True)
class Observation:
    outcome_id: str
    metric_name: str
    value: float
    note: str
    evidence_artifact_id: str | None = None
    observed_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.outcome_id or not self.metric_name.strip() or not self.note.strip():
            raise ValueError("Observation outcome, metric, and evidence note are required")
        if not isfinite(self.value):
            raise ValueError("Observation value must be finite")
        datetime.fromisoformat(self.observed_at)


@dataclass(slots=True)
class RecalibrationDecision:
    outcome_id: str
    mode: RecalibrationMode
    status: OutcomeStatus
    observed_value: float
    actual_progress: float
    expected_progress: float
    trajectory_variance: float
    rationale: str
    directives: list[str]
    decided_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    id: str = field(default_factory=lambda: str(uuid4()))


class StrategicOutcomeEngine:
    MINIMUM_FUNDING_SCORE = 0.05
    HORIZONS = (
        (30, 0.15, "Resolve the highest-value uncertainty and prove traction."),
        (365, 0.65, "Compound distribution, economics, reusable capabilities, and trust."),
        (1460, 1.0, "Reach the portfolio north star with durable strategic option value."),
    )

    def plan(self, outcome: StrategicOutcome) -> StrategicPlan:
        horizons = []
        for days, nominal_progress, intent in self.HORIZONS:
            progress = min(1.0, nominal_progress * (1460 / outcome.deadline_days) ** 0.35)
            if days >= outcome.deadline_days:
                progress = 1.0
            horizons.append(
                HorizonMilestone(
                    days=days,
                    target_value=round(outcome.metric.value_at_progress(progress), 6),
                    target_progress=round(progress, 4),
                    intent=intent,
                )
            )

        remaining = outcome.capital_budget_minor
        allocations: list[BetAllocation] = []
        for bet in sorted(outcome.bets, key=lambda item: item.strategic_score, reverse=True):
            eligible = bet.strategic_score >= self.MINIMUM_FUNDING_SCORE
            allocated = min(bet.requested_cost_minor, remaining) if eligible else 0
            remaining -= allocated
            if allocated:
                rationale = "Funded by impact × confidence × reversibility × information value per cost."
            elif not eligible:
                rationale = "Held unfunded because evidence-adjusted strategic score is below threshold."
            else:
                rationale = "Held as an unfunded option after the capital envelope was exhausted."
            allocations.append(
                BetAllocation(
                    bet_id=bet.id,
                    title=bet.title,
                    strategic_score=bet.strategic_score,
                    allocated_minor=allocated,
                    rationale=rationale,
                )
            )
        return StrategicPlan(outcome.id, horizons, allocations, remaining)

    def recalibrate(
        self,
        outcome: StrategicOutcome,
        observations: list[Observation],
        *,
        as_of: datetime | None = None,
    ) -> RecalibrationDecision:
        matching = [item for item in observations if item.metric_name == outcome.metric.name]
        if not matching:
            raise ValueError("Recalibration requires an observation of the primary metric")
        latest = max(matching, key=lambda item: item.observed_at)
        observed_time = datetime.fromisoformat(latest.observed_at)
        created = datetime.fromisoformat(outcome.created_at)
        current_time = as_of or observed_time
        elapsed_days = max(0.0, (current_time - created).total_seconds() / 86_400)
        expected = min(1.0, elapsed_days / outcome.deadline_days)
        actual = outcome.metric.progress(latest.value)
        variance = actual - expected

        reached = actual >= 1.0
        if reached and latest.evidence_artifact_id:
            mode, status = RecalibrationMode.ACHIEVED, OutcomeStatus.ACHIEVED
            directives = ["Verify evidence integrity and preserve the mechanisms that caused success."]
        elif reached:
            mode, status = RecalibrationMode.CONTINUE, OutcomeStatus.AHEAD
            directives = [
                "Target value is reported but cannot be marked achieved without an evidence artifact.",
                "Attach a tenant-scoped ledger, analytics, or audit artifact and observe again.",
            ]
        elif variance >= 0.15:
            mode, status = RecalibrationMode.AMPLIFY, OutcomeStatus.AHEAD
            directives = [
                "Increase allocation only to mechanisms supported by observed evidence.",
                "Protect quality, trust, and capacity while scaling.",
            ]
        elif variance >= -0.1:
            mode, status = RecalibrationMode.CONTINUE, OutcomeStatus.ON_TRACK
            directives = [
                "Continue the highest-ranked funded bets.",
                "Run the next scheduled falsification test without expanding scope.",
            ]
        elif variance >= -0.3:
            mode, status = RecalibrationMode.ADAPT, OutcomeStatus.BEHIND
            directives = [
                "Reduce allocation to weak mechanisms and test the largest causal uncertainty.",
                "Prefer a reversible adaptation before adding capital.",
            ]
        else:
            mode, status = RecalibrationMode.PIVOT_OR_STOP, OutcomeStatus.CRITICAL
            directives = [
                "Pause scaling and invoke bet kill criteria.",
                "Present pivot, pause, and stop options to the accountable human owner.",
            ]
        return RecalibrationDecision(
            outcome_id=outcome.id,
            mode=mode,
            status=status,
            observed_value=latest.value,
            actual_progress=round(actual, 6),
            expected_progress=round(expected, 6),
            trajectory_variance=round(variance, 6),
            rationale=(
                f"Observed progress {actual:.1%} versus time-indexed expectation {expected:.1%}; "
                "model-generated artifacts were not counted as progress."
            ),
            directives=directives,
        )


def outcome_to_dict(outcome: StrategicOutcome) -> dict[str, Any]:
    return asdict(outcome)


def outcome_from_dict(data: dict[str, Any]) -> StrategicOutcome:
    payload = dict(data)
    metric_data = dict(payload.pop("metric"))
    metric_data["direction"] = Direction(metric_data["direction"])
    bets = [StrategicBet(**item) for item in payload.pop("bets")]
    authority = AuthorityEnvelope(**payload.pop("authority"))
    payload["status"] = OutcomeStatus(payload.get("status", "active"))
    if payload.get("paused_from_status"):
        payload["paused_from_status"] = OutcomeStatus(payload["paused_from_status"])
    return StrategicOutcome(
        metric=Metric(**metric_data),
        bets=bets,
        authority=authority,
        **payload,
    )


def observation_from_dict(data: dict[str, Any]) -> Observation:
    return Observation(**data)
