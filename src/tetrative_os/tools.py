from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SideEffect(str, Enum):
    NONE = "none"
    REVERSIBLE = "reversible"
    IRREVERSIBLE = "irreversible"


@dataclass(frozen=True, slots=True)
class ToolPolicy:
    name: str
    description: str
    side_effect: SideEffect
    required_capability: str
    requires_approval: bool = True
    allowed_input_keys: frozenset[str] = field(default_factory=frozenset)
    max_cost_minor_units: int = 0


@dataclass(slots=True)
class ToolInvocation:
    tool: str
    input: dict[str, Any]
    capability: str | None = None
    approval_artifact_hash: str | None = None
    idempotency_key: str | None = None
    dry_run: bool = True


class ToolPolicyError(PermissionError):
    pass


class ToolRegistry:
    """Fail-closed capability registry. MVP registers read-only/dry-run tools only."""

    def __init__(self) -> None:
        self._tools: dict[str, tuple[ToolPolicy, Callable[[dict[str, Any]], Any]]] = {}
        self._completed_keys: dict[str, Any] = {}

    def register(self, policy: ToolPolicy, handler: Callable[[dict[str, Any]], Any]) -> None:
        if policy.name in self._tools:
            raise ValueError(f"Tool {policy.name!r} is already registered")
        if policy.side_effect is not SideEffect.NONE and not policy.requires_approval:
            raise ValueError("Side-effecting tools must require approval")
        self._tools[policy.name] = (policy, handler)

    def describe(self) -> list[ToolPolicy]:
        return [entry[0] for entry in self._tools.values()]

    def invoke(self, invocation: ToolInvocation) -> Any:
        entry = self._tools.get(invocation.tool)
        if entry is None:
            raise ToolPolicyError(f"Tool {invocation.tool!r} is not registered")
        policy, handler = entry
        unknown = set(invocation.input) - set(policy.allowed_input_keys)
        if unknown:
            raise ToolPolicyError(f"Tool input contains unknown keys: {sorted(unknown)}")
        if invocation.capability != policy.required_capability:
            raise ToolPolicyError("Missing or invalid tool capability")
        if policy.requires_approval and not invocation.approval_artifact_hash:
            raise ToolPolicyError("Tool requires an approved artifact hash")
        if policy.side_effect is not SideEffect.NONE:
            if not invocation.idempotency_key:
                raise ToolPolicyError("Side-effecting tool requires an idempotency key")
            if invocation.idempotency_key in self._completed_keys:
                return self._completed_keys[invocation.idempotency_key]
            if not invocation.dry_run:
                raise ToolPolicyError("External side effects are disabled in the current release")
        result = handler(invocation.input)
        if invocation.idempotency_key:
            self._completed_keys[invocation.idempotency_key] = result
        return result
