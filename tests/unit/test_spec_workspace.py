import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    "docs/01-engineering-intent",
    "docs/02-product-requirements",
    "docs/03-technical-spec",
    "docs/04-api-and-data-design",
    "docs/05-test-specification",
    "docs/06-security-and-reliability",
    "docs/07-deployment-and-monitoring",
    "docs/08-maintenance-and-spec-drift",
    "tasks/agent-task-list.md",
    "tasks/review-notes.md",
    "tests/unit",
    "tests/integration",
    "tests/end_to_end",
    "tests/adversarial",
    "changelog/CHANGELOG.md",
    "release-notes.md",
]


class SpecificationWorkspaceTests(unittest.TestCase):
    def test_required_specification_areas_exist(self):
        missing = [path for path in REQUIRED if not (ROOT / path).exists()]
        self.assertEqual(missing, [])

    def test_relative_markdown_links_resolve(self):
        broken = []
        pattern = re.compile(r"\[[^]]*]\(([^)]+)\)")
        for document in ROOT.rglob("*.md"):
            for target in pattern.findall(document.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                relative = target.split("#", 1)[0]
                if relative and not (document.parent / relative).resolve().exists():
                    broken.append(f"{document.relative_to(ROOT)} -> {target}")
        self.assertEqual(broken, [])


if __name__ == "__main__":
    unittest.main()
