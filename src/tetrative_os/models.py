from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class Risk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(slots=True)
class Goal:
    objective: str
    domain: str = "meta"
    audience: str = "unspecified"
    constraints: list[str] = field(default_factory=list)
    success_metrics: list[str] = field(default_factory=list)
    risk: Risk = Risk.MEDIUM
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        self.objective = self.objective.strip()
        self.audience = self.audience.strip()
        if not self.objective:
            raise ValueError("Goal objective cannot be empty")
        if len(self.objective) > 10_000:
            raise ValueError("Goal objective exceeds 10,000 characters")
        if len(self.constraints) > 100 or len(self.success_metrics) > 100:
            raise ValueError("Goal accepts at most 100 constraints and 100 success metrics")
        if sum(map(len, self.constraints)) > 50_000:
            raise ValueError("Goal constraints exceed the 50,000 character context budget")
        if sum(map(len, self.success_metrics)) > 10_000:
            raise ValueError("Goal success metrics exceed the 10,000 character context budget")


@dataclass(slots=True)
class AgentSpec:
    name: str
    role: str
    system_prompt: str
    tools: tuple[str, ...] = ()
    can_approve: bool = False


@dataclass(slots=True)
class Stage:
    name: str
    owner: str
    instruction: str
    depends_on: tuple[str, ...] = ()
    human_gate: bool = False
    minimum_score: float = 0.70


@dataclass(slots=True)
class Candidate:
    content: str
    author: str
    score: float = 0.0
    critique: str = ""
    iteration: int = 0
    policy_findings: list[dict[str, str]] = field(default_factory=list)


@dataclass(slots=True)
class StageResult:
    stage: str
    status: str
    selected: Candidate
    candidates: list[Candidate]
    attempts: int
    human_gate: bool = False


@dataclass(slots=True)
class RunResult:
    run_id: str
    goal: Goal
    status: str
    stages: list[StageResult]
    final_output: str
    metrics: dict[str, Any]
    started_at: str
    finished_at: str
    approval_required: dict[str, str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
