import unittest

from tetrative_os.evaluation import Evaluator
from tetrative_os.models import Candidate, Goal, Stage
from tetrative_os.providers import DeterministicMockProvider


class GroundingEvaluationTests(unittest.TestCase):
    def test_grounded_run_penalizes_missing_citation(self):
        provider = DeterministicMockProvider()
        evaluator = Evaluator(provider, "judge", "red team")
        goal = Goal(
            "Assess evidence",
            constraints=["SOURCE-GROUNDED EVIDENCE. Cite [S#]."],
        )
        stage = Stage("evidence", "researcher", "Assess")
        uncited = Candidate(
            "## Decision\nValidate the metric with a test.\n## Risks\nUnknown assumption and failure risk.",
            "researcher",
        )
        cited = Candidate(
            "## Decision\nValidate the metric with a test using observed evidence [S1].\n"
            "## Risks\nUnknown assumption and failure risk.",
            "researcher",
        )
        uncited_score = evaluator.assess(goal, stage, uncited)
        cited_score = evaluator.assess(goal, stage, cited)
        self.assertEqual(uncited_score.details["citation_grounding"], 0.0)
        self.assertEqual(cited_score.details["citation_grounding"], 1.0)
        self.assertGreater(cited_score.total, uncited_score.total)


if __name__ == "__main__":
    unittest.main()
