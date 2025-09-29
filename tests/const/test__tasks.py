import pytest

from const import Tasks


class TestTasks:
    """Test suite for the Tasks."""

    @pytest.mark.parametrize(
        ("task", "expected"),
        [
            (Tasks.FEATUREENGINEERING, "feature-engineering"),
            (Tasks.TRAING, "training"),
            (Tasks.EVALUATION, "evaluation"),
            (Tasks.INFERENCE, "inference"),
            (Tasks.EXPORT, "export"),
        ],
    )
    def test_all(self, task: Tasks, expected: str) -> None:
        """Test All Tasks."""
        if task != expected:
            pytest.fail(f"Expected '{expected}', but got '{task}'")
