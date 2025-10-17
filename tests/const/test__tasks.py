import pytest

from const import Task


class TestTasks:
    """Test suite for the Task."""

    @pytest.mark.parametrize(
        ("task", "expected"),
        [
            (Task.FEATURE_ENGINEERING, "feature_engineering"),
            (Task.TRAING, "training"),
            (Task.EVALUATION, "evaluation"),
            (Task.INFERENCE, "inference"),
            (Task.EXPORT, "export"),
        ],
    )
    def test_all(self, task: Task, expected: str) -> None:
        """Test All Tasks."""
        if task != expected:
            pytest.fail(f"Expected '{expected}', but got '{task}'")
