import unittest
from datetime import UTC, datetime, timedelta

from tetrative_os.autonomy import ActionProposal, Authorization, AutonomyController
from tetrative_os.outcomes import (
    AuthorityEnvelope,
    Direction,
    Metric,
    Observation,
    RecalibrationMode,
    StrategicBet,
    StrategicOutcome,
    StrategicOutcomeEngine,
)


def outcome() -> StrategicOutcome:
    return StrategicOutcome(
        title="Build a profitable creator venture portfolio",
        north_star="Reach repeatable revenue with trusted distribution",
        owner="founder",
        metric=Metric("monthly recurring revenue", "NGN", 0, 10_000_000),
        capital_budget_minor=1_000_000,
        guardrails=["No deceptive claims", "Human approval for protected actions"],
        bets=[
            StrategicBet(
                "Design partner sprint",
                "growth",
                "Paid design partners reveal the strongest wedge",
                0.8,
                0.7,
                400_000,
                True,
                "Stop if fewer than three qualified calls from 100 targeted contacts",
            ),
            StrategicBet(
                "National advertising",
                "marketing",
                "Broad reach creates demand",
                0.9,
                0.2,
                900_000,
                False,
                "Stop if incrementality is below five percent",
            ),
        ],
        authority=AuthorityEnvelope(
            allowed_tools=["analytics.read", "experiment.configure", "publisher.preview"],
            max_risk="medium",
            total_spend_minor=100_000,
            approval_spend_threshold_minor=20_000,
        ),
    )


class StrategicOutcomeTests(unittest.TestCase):
    def test_plan_materializes_all_horizons_and_respects_capital(self):
        contract = outcome()
        plan = StrategicOutcomeEngine().plan(contract)
        self.assertEqual([item.days for item in plan.horizons], [30, 365, 1460])
        self.assertLessEqual(
            sum(item.allocated_minor for item in plan.allocations),
            contract.capital_budget_minor,
        )
        self.assertEqual(plan.allocations[0].title, "Design partner sprint")
        self.assertGreater(plan.allocations[0].strategic_score, plan.allocations[1].strategic_score)
        self.assertEqual(plan.allocations[1].allocated_minor, 0)
        self.assertEqual(plan.unallocated_minor, 600_000)

    def test_metric_direction_validation_and_minimize_progress(self):
        with self.assertRaises(ValueError):
            Metric("cost", "NGN", 100, 50, Direction.MAXIMIZE)
        metric = Metric("cost", "NGN", 100, 50, Direction.MINIMIZE)
        self.assertEqual(metric.progress(75), 0.5)

    def test_achievement_requires_an_evidence_artifact(self):
        contract = outcome()
        reported = Observation(
            contract.id,
            contract.metric.name,
            contract.metric.target,
            "Self-reported target",
        )
        unverified = StrategicOutcomeEngine().recalibrate(contract, [reported])
        self.assertNotEqual(unverified.mode, RecalibrationMode.ACHIEVED)
        reported.evidence_artifact_id = "verified-ledger-artifact"
        verified = StrategicOutcomeEngine().recalibrate(contract, [reported])
        self.assertEqual(verified.mode, RecalibrationMode.ACHIEVED)

    def test_recalibration_uses_observation_not_agent_output(self):
        contract = outcome()
        contract.created_at = (datetime.now(UTC) - timedelta(days=365)).isoformat()
        observation = Observation(
            contract.id,
            contract.metric.name,
            1_000_000,
            "Verified ledger value",
        )
        decision = StrategicOutcomeEngine().recalibrate(contract, [observation])
        self.assertEqual(decision.mode, RecalibrationMode.ADAPT)
        self.assertAlmostEqual(decision.actual_progress, 0.1)
        self.assertIn("model-generated artifacts were not counted", decision.rationale)


class AutonomyControllerTests(unittest.TestCase):
    def test_low_risk_reversible_action_inside_envelope_is_allowed(self):
        envelope = outcome().authority
        proposal = ActionProposal(
            outcome_id="outcome",
            tool="experiment.configure",
            category="experiment",
            risk="low",
            estimated_spend_minor=10_000,
            reversible=True,
            external_effect=True,
            expected_effect="Create a reversible holdout",
            rollback="Delete the draft experiment",
            idempotency_key="experiment-1",
        )
        decision = AutonomyController().decide(proposal, envelope)
        self.assertEqual(decision.authorization, Authorization.ALLOW)

    def test_protected_or_expensive_action_requires_approval(self):
        envelope = outcome().authority
        envelope.allowed_tools.append("publisher.publish")
        proposal = ActionProposal(
            outcome_id="outcome",
            tool="publisher.publish",
            category="experiment",
            risk="medium",
            estimated_spend_minor=30_000,
            reversible=True,
            external_effect=True,
            expected_effect="Publish campaign",
            rollback="Unpublish campaign",
            idempotency_key="publish-1",
        )
        decision = AutonomyController().decide(proposal, envelope)
        self.assertEqual(decision.authorization, Authorization.REQUIRE_APPROVAL)
        self.assertTrue(decision.requires_human)

    def test_kill_switch_and_budget_fail_closed(self):
        envelope = outcome().authority
        envelope.kill_switch = True
        proposal = ActionProposal(
            outcome_id="outcome",
            tool="analytics.read",
            category="analytics",
            risk="low",
            estimated_spend_minor=200_000,
            reversible=True,
            external_effect=False,
            expected_effect="Read a metric",
            rollback="No external effect",
        )
        decision = AutonomyController().decide(proposal, envelope)
        self.assertEqual(decision.authorization, Authorization.DENY)
        self.assertTrue(any("kill switch" in reason for reason in decision.reasons))
        self.assertTrue(any("spend" in reason for reason in decision.reasons))


if __name__ == "__main__":
    unittest.main()
