import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from tetrative_os.api import Principal, Settings, create_app


def contract_payload() -> dict:
    return {
        "title": "Creator venture portfolio",
        "north_star": "Build repeatable revenue through trusted distribution",
        "metric": {
            "name": "monthly recurring revenue",
            "unit": "NGN",
            "baseline": 0,
            "target": 10000000,
            "direction": "maximize",
        },
        "capital_budget_minor": 1000000,
        "guardrails": ["No deceptive claims", "Protect customer identity"],
        "bets": [
            {
                "title": "Design partner sprint",
                "owner": "growth",
                "hypothesis": "Paid partners reveal the strongest wedge",
                "expected_impact": 0.8,
                "confidence": 0.7,
                "requested_cost_minor": 400000,
                "reversible": True,
                "kill_criterion": "Stop below three qualified calls",
                "evidence": [],
            },
            {
                "title": "Founder UGC experiment",
                "owner": "content",
                "hypothesis": "Founder proof increases qualified response",
                "expected_impact": 0.6,
                "confidence": 0.5,
                "requested_cost_minor": 200000,
                "reversible": True,
                "kill_criterion": "Stop below two percent qualified response",
                "evidence": [],
            },
        ],
        "authority": {
            "allowed_tools": ["analytics.read", "experiment.configure", "publisher.publish"],
            "max_risk": "medium",
            "total_spend_minor": 100000,
            "approval_spend_threshold_minor": 20000,
            "max_actions_per_day": 10,
        },
        "deadline_days": 1460,
    }


class StrategicOutcomeApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.client = TestClient(
            create_app(
                Settings(
                    environment="test",
                    principals={
                        "v220-admin": Principal("strategist", "portfolio", frozenset({"admin"}))
                    },
                    data_dir=Path(self.temp.name),
                    default_mock=True,
                    cors_origins=(),
                )
            )
        )
        self.headers = {"Authorization": "Bearer v220-admin"}

    def tearDown(self):
        self.client.close()
        self.temp.cleanup()

    def test_outcome_observation_action_and_linked_run_journey(self):
        created = self.client.post(
            "/api/v220/outcomes", headers=self.headers, json=contract_payload()
        )
        self.assertEqual(created.status_code, 200, created.text)
        payload = created.json()
        outcome_id = payload["outcome"]["id"]
        self.assertEqual(len(payload["plan"]["horizons"]), 3)
        self.assertLessEqual(
            sum(item["allocated_minor"] for item in payload["plan"]["allocations"]),
            contract_payload()["capital_budget_minor"],
        )

        observation = self.client.post(
            f"/api/v220/outcomes/{outcome_id}/observations",
            headers=self.headers,
            json={
                "metric_name": "monthly recurring revenue",
                "value": 2000000,
                "note": "Verified billing ledger",
            },
        )
        self.assertEqual(observation.status_code, 200, observation.text)
        self.assertEqual(observation.json()["recalibration"]["mode"], "amplify")

        action = {
            "tool": "experiment.configure",
            "category": "experiment",
            "risk": "low",
            "estimated_spend_minor": 10000,
            "reversible": True,
            "external_effect": True,
            "expected_effect": "Create a reversible holdout experiment",
            "rollback": "Delete the draft experiment",
            "idempotency_key": "holdout-001",
        }
        authorized = self.client.post(
            f"/api/v220/outcomes/{outcome_id}/actions/authorize",
            headers=self.headers,
            json=action,
        )
        self.assertEqual(authorized.status_code, 200, authorized.text)
        self.assertEqual(authorized.json()["decision"]["authorization"], "allow")
        replay = self.client.post(
            f"/api/v220/outcomes/{outcome_id}/actions/authorize",
            headers=self.headers,
            json=action,
        ).json()
        self.assertTrue(replay["replayed"])
        self.assertEqual(replay["proposal"]["id"], authorized.json()["proposal"]["id"])
        conflicting = dict(action)
        conflicting["expected_effect"] = "A different effect with the reused key"
        conflict = self.client.post(
            f"/api/v220/outcomes/{outcome_id}/actions/authorize",
            headers=self.headers,
            json=conflicting,
        )
        self.assertEqual(conflict.status_code, 409)

        linked = self.client.post(
            "/api/v1/runs",
            headers=self.headers,
            json={
                "objective": "Build the strategic execution campaign",
                "domain": "outcome",
                "outcome_id": outcome_id,
                "mock": True,
                "auto_approve": True,
            },
        )
        self.assertEqual(linked.status_code, 200, linked.text)
        self.assertEqual(linked.json()["status"], "completed")

        stopped = self.client.post(
            f"/api/v220/outcomes/{outcome_id}/kill-switch",
            headers=self.headers,
            json={"enabled": True, "reason": "Operator requested an emergency pause"},
        )
        self.assertEqual(stopped.status_code, 200, stopped.text)
        self.assertEqual(stopped.json()["status"], "paused")
        paused_observation = self.client.post(
            f"/api/v220/outcomes/{outcome_id}/observations",
            headers=self.headers,
            json={
                "metric_name": "monthly recurring revenue",
                "value": 3000000,
                "note": "Observation while operational authority is paused",
            },
        )
        self.assertEqual(paused_observation.status_code, 200)
        paused_detail = self.client.get(
            f"/api/v220/outcomes/{outcome_id}", headers=self.headers
        ).json()
        self.assertEqual(paused_detail["status"], "paused")
        blocked_run = self.client.post(
            "/api/v1/runs",
            headers=self.headers,
            json={
                "objective": "This linked run must not start",
                "domain": "outcome",
                "outcome_id": outcome_id,
                "mock": True,
            },
        )
        self.assertEqual(blocked_run.status_code, 423)
        resumed = self.client.post(
            f"/api/v220/outcomes/{outcome_id}/kill-switch",
            headers=self.headers,
            json={"enabled": False, "reason": "Incident resolved and authority reviewed"},
        )
        self.assertEqual(resumed.json()["status"], "ahead")

        detail = self.client.get(
            f"/api/v220/outcomes/{outcome_id}", headers=self.headers
        ).json()
        self.assertEqual(len(detail["observations"]), 2)
        self.assertTrue(any(item["kind"] == "recalibration" for item in detail["decisions"]))
        self.assertTrue(any(item["kind"] == "agent_run" for item in detail["decisions"]))
        self.assertEqual(len(detail["actions"]), 1)

    def test_protected_action_requires_approval_and_kill_switch_denies(self):
        body = contract_payload()
        body["authority"]["kill_switch"] = True
        created = self.client.post("/api/v220/outcomes", headers=self.headers, json=body).json()
        outcome_id = created["outcome"]["id"]
        response = self.client.post(
            f"/api/v220/outcomes/{outcome_id}/actions/authorize",
            headers=self.headers,
            json={
                "tool": "publisher.publish",
                "category": "publish",
                "risk": "medium",
                "estimated_spend_minor": 30000,
                "reversible": True,
                "external_effect": True,
                "expected_effect": "Publish approved campaign",
                "rollback": "Unpublish campaign",
                "idempotency_key": "publish-001",
            },
        )
        self.assertEqual(response.json()["decision"]["authorization"], "deny")
        self.assertTrue(
            any("kill switch" in reason for reason in response.json()["decision"]["reasons"])
        )


if __name__ == "__main__":
    unittest.main()
