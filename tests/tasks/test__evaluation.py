import pytest

from tasks import EvaluationTask
from tasks.evaluation.settings import EvaluationSettings


class TestEvaluationTask:
    """Test suite for the EvaluationTask."""

    def setup_method(self) -> None:
        """Set up BaseTask."""
        self.task = EvaluationTask()  # type:ignore[reportAbstractUsage]

    def test_settings(self) -> None:
        """Test Settings for EvaluationTask."""
        if not isinstance(self.task.settings, EvaluationSettings):
            pytest.fail(
                f"Expected {EvaluationSettings}, but got {type(self.task.settings)}"
            )

    def test_run(self) -> None:
        """Test run method for EvaluationTask."""
        self.task.run()


class TestEvaluationSettings:
    """Test suite for EvaluationSettings."""
