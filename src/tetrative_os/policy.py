from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from enum import Enum

from .models import Goal, Risk, Stage


class Severity(str, Enum):
    WARNING = "warning"
    BLOCK = "block"


@dataclass(frozen=True, slots=True)
class PolicyFinding:
    rule_id: str
    severity: Severity
    message: str
    remediation: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PolicyReport:
    findings: tuple[PolicyFinding, ...] = ()

    @property
    def blocked(self) -> bool:
        return any(finding.severity is Severity.BLOCK for finding in self.findings)

    def as_prompt(self) -> str:
        if not self.findings:
            return "No deterministic policy findings."
        return "\n".join(
            f"- {finding.rule_id} [{finding.severity.value}]: {finding.message} "
            f"Remediation: {finding.remediation}"
            for finding in self.findings
        )


class PolicyEngine:
    """Narrow deterministic gates for critical execution invariants.

    These rules intentionally avoid broad semantic moderation. They enforce requirements that can be
    tested reliably and leave nuanced judgments to versioned evals and authenticated humans.
    """

    _bypass = re.compile(
        r"\b(?:bypass|skip|disable|ignore)\b.{0,50}\b(?:approval|safeguard|safety review|policy)\b",
        re.IGNORECASE | re.DOTALL,
    )
    _identity = re.compile(
        r"\b(?:impersonat\w*|deepfake|clone(?:d|s|ing)?\s+(?:their|a|the)?\s*(?:voice|face|likeness))\b",
        re.IGNORECASE,
    )
    _negation = re.compile(r"\b(?:never|do not|don't|must not|cannot|prohibit(?:ed)?|avoid)\b", re.IGNORECASE)
    _guarantee = re.compile(r"\b(?:guaranteed?|100% certain|cannot fail|zero risk)\b", re.IGNORECASE)

    def evaluate(self, goal: Goal, stage: Stage, content: str) -> PolicyReport:
        findings: list[PolicyFinding] = []
        if self._unsafe_match(self._bypass, content):
            findings.append(
                PolicyFinding(
                    "POL-001",
                    Severity.BLOCK,
                    "Output recommends bypassing approval, policy, or a safety safeguard.",
                    "Require the applicable authenticated approval and preserve the safeguard.",
                )
            )
        if self._unsafe_match(self._identity, content) and not re.search(
            r"\b(?:consent|permission|authorized|rights release)\b", content, re.IGNORECASE
        ):
            findings.append(
                PolicyFinding(
                    "POL-002",
                    Severity.BLOCK,
                    "Identity, likeness, face, or voice simulation lacks explicit consent controls.",
                    "Remove impersonation or require verified consent and rights provenance.",
                )
            )

        grounded = any("SOURCE-GROUNDED EVIDENCE" in item for item in goal.constraints)
        if grounded and not re.search(r"\[S\d+]", content):
            findings.append(
                PolicyFinding(
                    "POL-003",
                    Severity.BLOCK,
                    "A source-grounded run produced an output without a source citation.",
                    "Cite supplied evidence as [S#] or label the statement as an unsupported assumption.",
                )
            )

        if goal.domain in {"ugc", "ecosystem"} and stage.name in {"production_plan", "ugc_engine"}:
            if not re.search(
                r"\b(?:consent|rights|license|licensed|release form|intellectual property|copyright)\b",
                content,
                re.IGNORECASE,
            ):
                findings.append(
                    PolicyFinding(
                        "UGC-001",
                        Severity.BLOCK,
                        "Production plan omits media, likeness, or intellectual-property rights controls.",
                        "Add consent, rights-release, licensing, and provenance checks.",
                    )
                )
            if not re.search(
                r"\b(?:disclos\w*|sponsored|synthetic media|ai-generated|paid partnership)\b",
                content,
                re.IGNORECASE,
            ):
                findings.append(
                    PolicyFinding(
                        "UGC-002",
                        Severity.BLOCK,
                        "Production plan omits synthetic or commercial disclosure controls.",
                        "Specify platform-appropriate AI, sponsorship, and material-connection disclosures.",
                    )
                )

        if goal.risk in {Risk.HIGH, Risk.CRITICAL} and stage.human_gate:
            if not re.search(r"\b(?:human|reviewer|operator)\s+approv\w*", content, re.IGNORECASE):
                findings.append(
                    PolicyFinding(
                        "RISK-001",
                        Severity.BLOCK,
                        "High-risk execution plan does not explicitly require human approval.",
                        "Add a named human approval gate before every consequential action.",
                    )
                )
            if not re.search(r"\b(?:rollback|stop condition|kill criterion|escalat\w*)\b", content, re.IGNORECASE):
                findings.append(
                    PolicyFinding(
                        "RISK-002",
                        Severity.BLOCK,
                        "High-risk execution plan lacks stop, rollback, or escalation behavior.",
                        "Define measurable stop conditions, rollback steps, and escalation ownership.",
                    )
                )

        if self._unsafe_match(self._guarantee, content):
            findings.append(
                PolicyFinding(
                    "CLAIM-001",
                    Severity.WARNING,
                    "Output uses absolute guarantee language that may overstate uncertain outcomes.",
                    "Replace the guarantee with calibrated probability, evidence, and limitations.",
                )
            )
        return PolicyReport(tuple(findings))

    def _unsafe_match(self, pattern: re.Pattern[str], content: str) -> bool:
        for match in pattern.finditer(content):
            prefix = content[max(0, match.start() - 35) : match.start()]
            if not self._negation.search(prefix):
                return True
        return False
