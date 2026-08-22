import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from tetrative_os.api import Principal, Settings, create_app


class ApiIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        settings = Settings(
            environment="test",
            principals={
                "test-key-with-enough-entropy": Principal(
                    "test-admin", "test-tenant", frozenset({"admin"})
                )
            },
            data_dir=Path(self.temp.name),
            default_mock=True,
            cors_origins=(),
        )
        self.client = TestClient(create_app(settings))
        self.headers = {"Authorization": "Bearer test-key-with-enough-entropy"}

    def tearDown(self):
        self.client.close()
        self.temp.cleanup()

    def test_health_is_public_but_runs_require_auth(self):
        self.assertEqual(self.client.get("/healthz").status_code, 200)
        self.assertEqual(self.client.get("/api/v1/runs").status_code, 401)
        self.assertEqual(
            self.client.get("/api/v1/runs", headers={"Authorization": "Bearer wrong"}).status_code,
            403,
        )

    def test_production_configuration_rejects_auto_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            client = TestClient(
                create_app(
                    Settings(
                        environment="production",
                        principals={
                            "production-key-with-enough-entropy": Principal(
                                "production-admin", "production", frozenset({"admin"})
                            )
                        },
                        data_dir=Path(directory),
                        default_mock=True,
                        cors_origins=(),
                    )
                )
            )
            response = client.post(
                "/api/v1/runs",
                headers={"Authorization": "Bearer production-key-with-enough-entropy"},
                json={"objective": "Do not bypass review", "auto_approve": True},
            )
            self.assertEqual(response.status_code, 403)
            client.close()

    def test_roles_and_tenant_boundaries_are_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings(
                environment="test",
                principals={
                    "alpha-operator": Principal(
                        "alpha-operator", "alpha", frozenset({"operator"})
                    ),
                    "alpha-approver": Principal(
                        "alpha-approver", "alpha", frozenset({"approver"})
                    ),
                    "beta-viewer": Principal("beta-viewer", "beta", frozenset({"viewer"})),
                },
                data_dir=Path(directory),
                default_mock=True,
                cors_origins=(),
            )
            client = TestClient(create_app(settings))
            operator_headers = {"Authorization": "Bearer alpha-operator"}
            approver_headers = {"Authorization": "Bearer alpha-approver"}
            beta_headers = {"Authorization": "Bearer beta-viewer"}
            paused = client.post(
                "/api/v1/runs",
                headers=operator_headers,
                json={"objective": "Tenant-scoped UGC", "domain": "ugc", "mock": True},
            ).json()
            denied = client.post(
                f"/api/v1/runs/{paused['run_id']}/approve?mock=true",
                headers=operator_headers,
                json={"artifact_hash": paused["approval_required"]["artifact_hash"]},
            )
            self.assertEqual(denied.status_code, 403)
            self.assertEqual(
                client.get(f"/api/v1/runs/{paused['run_id']}", headers=beta_headers).status_code,
                404,
            )
            exported = client.post(
                f"/api/v1/runs/{paused['run_id']}/exports/ugc", headers=operator_headers
            ).json()
            self.assertEqual(
                client.get(
                    f"/api/v1/artifacts/{exported['id']}", headers=beta_headers
                ).status_code,
                404,
            )
            approved = client.post(
                f"/api/v1/runs/{paused['run_id']}/approve?mock=true",
                headers=approver_headers,
                json={"artifact_hash": paused["approval_required"]["artifact_hash"]},
            )
            self.assertEqual(approved.status_code, 200, approved.text)
            detail = client.get(
                f"/api/v1/runs/{paused['run_id']}", headers=approver_headers
            ).json()
            approval = next(event for event in detail["events"] if event["kind"] == "human_approved")
            self.assertEqual(approval["payload"]["approver"], "alpha-approver")
            client.close()

    def test_run_approval_and_ugc_export_journey(self):
        created = self.client.post(
            "/api/v1/runs",
            headers=self.headers,
            json={
                "objective": "Create a reviewed UGC launch package",
                "domain": "ugc",
                "audience": "Nigerian SaaS founders",
                "success_metrics": ["ten qualified replies"],
                "mock": True,
            },
        )
        self.assertEqual(created.status_code, 200, created.text)
        paused = created.json()
        self.assertEqual(paused["status"], "awaiting_human_approval")

        listed = self.client.get("/api/v1/runs", headers=self.headers).json()
        self.assertEqual(listed[0]["run_id"], paused["run_id"])

        approved = self.client.post(
            f"/api/v1/runs/{paused['run_id']}/approve?mock=true",
            headers=self.headers,
            json={
                "artifact_hash": paused["approval_required"]["artifact_hash"],
            },
        )
        self.assertEqual(approved.status_code, 200, approved.text)
        self.assertEqual(approved.json()["status"], "completed")

        exported = self.client.post(
            f"/api/v1/runs/{paused['run_id']}/exports/ugc", headers=self.headers
        )
        self.assertEqual(exported.status_code, 200, exported.text)
        artifact = exported.json()
        download = self.client.get(
            f"/api/v1/artifacts/{artifact['id']}", headers=self.headers
        )
        self.assertEqual(download.status_code, 200)
        self.assertEqual(download.headers["content-type"], "application/zip")
        self.assertGreater(len(download.content), 100)


if __name__ == "__main__":
    unittest.main()
