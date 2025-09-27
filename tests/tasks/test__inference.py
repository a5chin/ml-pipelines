import pytest

from tasks import InferenceTask
from tasks.inference.settings import InferenceSettings


class TestInference:
    """Test suite for the InferenceTask."""

    def setup_method(self) -> None:
        """Set up BaseTask."""
        self.task = InferenceTask()  # type:ignore[reportAbstractUsage]

    def test_settings(self) -> None:
        """Test Settings for InferenceTask."""
        if not isinstance(self.task.settings, InferenceSettings):
            pytest.fail(
                f"Expected {InferenceSettings}, but got {type(self.task.settings)}"
            )

    def test_run(self) -> None:
        """Test run method for InferenceTask."""
        self.task.run()


class TestInferenceSettings:
    """Test suite for InferenceSettings."""
