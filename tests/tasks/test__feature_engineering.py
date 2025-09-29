import pytest

from tasks import FeatureEngineeringTask
from tasks.feature_engineering.settings import FeatureEngineeringSettings


class TestFeatureEngineeringTask:
    """Test suite for the FeatureEngineeringTask."""

    def setup_method(self) -> None:
        """Set up BaseTask."""
        self.task = FeatureEngineeringTask()  # type:ignore[reportAbstractUsage]

    def test_settings(self) -> None:
        """Test Settings for FeatureEngineeringTask."""
        if not isinstance(self.task.settings, FeatureEngineeringSettings):
            pytest.fail(
                f"Expected {FeatureEngineeringSettings}, "
                "but got {type(self.task.settings)}"
            )

    def test_run(self) -> None:
        """Test run method for FeatureEngineeringTask."""
        self.task.run()


class TestFeatureEngineeringSettings:
    """Test suite for FeatureEngineeringSettings."""
