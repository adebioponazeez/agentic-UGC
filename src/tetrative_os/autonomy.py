from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from uuid import uuid4

from .outcomes import AuthorityEnvelope


class Authorization(str, Enum):
    ALLOW = "allow"
    REQUIRE_APPROVAL = "require_approval"
    DENY = "deny"


RISK_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}


@dataclass(slots=True)
class ActionProposal:
    outcome_id: str
    tool: str
    category: str
    risk: str
    estimated_spend_minor: int
    reversible: bool
    external_effect: bool
    expected_effect: str
    rollback: str
    idempotency_key: str | None = None
    id: str = ""

    def __post_init__(self) -> None:
        self.id = self.id or str(uuid4())
        self.tool = self.tool.strip().lower()
        self.category = self.category.strip().lower()
        if self.risk not in RISK_ORDER:
            raise ValueError("Action risk is invalid")
        if self.estimated_spend_minor < 0:
            raise ValueError("Action spend cannot be negative")
        if not self.tool.strip() or not self.category.strip() or not self.expected_effect.strip():
            raise ValueError("Action tool, category, and expected effect are required")


@dataclass(slots=True)
class AutonomyDecision:
    action_id: str
    outcome_id: str
    authorization: Authorization
    reasons: list[str]
    remaining_spend_minor: int
    requires_human: bool

    def to_dict(self) -> dict:
        return asdict(self)


class AutonomyController:
    """Authorize proposals against pre-approved authority; never executes the effect."""

    def decide(
        self,
        proposal: ActionProposal,
        envelope: AuthorityEnvelope,
        *,
        spent_minor: int = 0,
        actions_today: int = 0,
    ) -> AutonomyDecision:
        deny: list[str] = []
        approval: list[str] = []
        if envelope.kill_switch:
            deny.append("AUTH-001: authority kill switch is active")
        if proposal.tool not in envelope.allowed_tools:
            deny.append("AUTH-002: tool is outside the allowed capability set")
        if RISK_ORDER[proposal.risk] > RISK_ORDER[envelope.max_risk]:
            deny.append("AUTH-003: action risk exceeds the authority ceiling")
        remaining = max(0, envelope.total_spend_minor - spent_minor)
        if proposal.estimated_spend_minor > remaining:
            deny.append("AUTH-004: action exceeds the remaining spend envelope")
        if actions_today >= envelope.max_actions_per_day:
            deny.append("AUTH-005: daily action-rate envelope is exhausted")
        if proposal.external_effect and not proposal.idempotency_key:
            deny.append("AUTH-006: external effects require an idempotency key")
        if proposal.reversible and not proposal.rollback.strip():
            deny.append("AUTH-007: reversible action lacks a rollback procedure")

        protected_tool_prefixes = (
            "payment.",
            "publisher.publish",
            "identity.",
            "message.send",
            "delete.",
            "contract.",
            "credential.",
            "deploy.production",
        )
        protected = proposal.category in envelope.protected_categories or proposal.tool.startswith(
            protected_tool_prefixes
        )
        if protected:
            approval.append("AUTH-101: protected action category requires human approval")
        if not proposal.reversible:
            approval.append("AUTH-102: irreversible action requires human approval")
        if proposal.estimated_spend_minor > envelope.approval_spend_threshold_minor:
            approval.append("AUTH-103: spend exceeds the autonomous approval threshold")
        if proposal.risk in {"high", "critical"}:
            approval.append("AUTH-104: high-impact action requires human approval")

        if deny:
            authorization = Authorization.DENY
            reasons = deny + approval
        elif approval:
            authorization = Authorization.REQUIRE_APPROVAL
            reasons = approval
        else:
            authorization = Authorization.ALLOW
            reasons = ["AUTH-000: action fits the active bounded-authority envelope"]
        return AutonomyDecision(
            action_id=proposal.id,
            outcome_id=proposal.outcome_id,
            authorization=authorization,
            reasons=reasons,
            remaining_spend_minor=max(0, remaining - proposal.estimated_spend_minor),
            requires_human=authorization is not Authorization.ALLOW,
        )
