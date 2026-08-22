import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tetrative_os.api import Principal, Settings, create_app
from tetrative_os.artifacts import ArtifactStore
from tetrative_os.memory import MemoryStore


class IdentityConfigurationTests(unittest.TestCase):
    def test_multi_principal_environment_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            encoded = json.dumps(
                {
                    "operator-secret-with-24-chars": {
                        "subject": "operator@example.com",
                        "tenant": "acme",
                        "roles": ["operator", "viewer"],
                    },
                    "approver-secret-with-24-chars": {
                        "subject": "approver@example.com",
                        "tenant": "acme",
                        "roles": ["approver", "viewer"],
                    },
                }
            )
            with patch.dict(
                os.environ,
                {
                    "TETRATIVE_ENV": "production",
                    "TETRATIVE_API_KEYS_JSON": encoded,
                    "TETRATIVE_DATA_DIR": directory,
                },
                clear=True,
            ):
                settings = Settings.from_env()
            self.assertEqual(len(settings.principals), 2)
            self.assertEqual(
                settings.principals["operator-secret-with-24-chars"].tenant, "acme"
            )

    def test_production_rejects_short_key(self):
        with tempfile.TemporaryDirectory() as directory:
            encoded = json.dumps(
                {
                    "short": {
                        "subject": "admin",
                        "tenant": "default",
                        "roles": ["admin"],
                    }
                }
            )
            with patch.dict(
                os.environ,
                {
                    "TETRATIVE_ENV": "production",
                    "TETRATIVE_API_KEYS_JSON": encoded,
                    "TETRATIVE_DATA_DIR": directory,
                },
                clear=True,
            ), self.assertRaises(RuntimeError):
                Settings.from_env()

    def test_principal_rejects_path_like_tenant(self):
        for tenant in ("../other", "/absolute", "has space", ""):
            with self.subTest(tenant=tenant), self.assertRaises(ValueError):
                Principal("subject", tenant, frozenset({"viewer"}))

    def test_v03_default_state_migrates_without_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            legacy_memory = MemoryStore(f"{directory}/memory.db")
            legacy_memory.record("legacy-run", "stage", "created", {"ok": True})
            legacy_memory.close()
            legacy_artifacts = ArtifactStore(f"{directory}/artifacts")
            artifact = legacy_artifacts.put(b"legacy", kind="legacy.v1", content_type="text/plain")
            settings = Settings(
                environment="test",
                principals={
                    "key": Principal("admin", "default", frozenset({"admin"}))
                },
                data_dir=Path(directory),
                default_mock=True,
                cors_origins=(),
            )
            create_app(settings)
            migrated = MemoryStore(f"{directory}/tenants/default/memory.db")
            try:
                self.assertEqual(migrated.events("legacy-run")[0]["payload"], {"ok": True})
            finally:
                migrated.close()
            _, content = ArtifactStore(f"{directory}/tenants/default/artifacts").get(artifact.id)
            self.assertEqual(content, b"legacy")


if __name__ == "__main__":
    unittest.main()
