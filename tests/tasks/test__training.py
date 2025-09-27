import pytest
from pydantic import ValidationError

from tasks import TrainingTask
from tasks.training.settings import TrainingSettings


class TestTrainingTask:
    """Test suite for the TrainingTask."""

    def setup_method(self) -> None:
        """Set up BaseTask."""
        self.task = TrainingTask()  # type:ignore[reportAbstractUsage]

    def test_settings(self) -> None:
        """Test Settings for TrainingTask."""
        if not isinstance(self.task.settings, TrainingSettings):
            pytest.fail(
                f"Expected {TrainingSettings}, but got {type(self.task.settings)}"
            )

    def test_run(self) -> None:
        """Test run method for TrainingTask."""
        self.task.run()


class TestTrainingSettings:
    """Test suite for TrainingSettings."""

    @pytest.mark.parametrize(
        ("seed", "error"),
        [
            (1, None),
            (42, None),
            (10.0, None),
            (-1, ValueError),
            (4.2, ValidationError),
            (0.1, ValidationError),
        ],
    )
    def test_seed(self, seed: int, error: type) -> None:
        """Test seed attribute (valid and invalid cases)."""
        if not error:
            _ = TrainingSettings(seed=seed)
            return

        with pytest.raises(error):
            TrainingSettings(seed=seed)
