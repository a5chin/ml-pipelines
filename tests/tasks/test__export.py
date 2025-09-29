import pytest

from tasks import ExportTask
from tasks.export.settings import ExportSettings


class TestExportTask:
    """Test suite for the ExportTask."""

    def setup_method(self) -> None:
        """Set up BaseTask."""
        self.task = ExportTask()  # type:ignore[reportAbstractUsage]

    def test_settings(self) -> None:
        """Test Settings for ExportTask."""
        if not isinstance(self.task.settings, ExportSettings):
            pytest.fail(
                f"Expected {ExportSettings}, but got {type(self.task.settings)}"
            )

    def test_run(self) -> None:
        """Test run method for ExportTask."""
        self.task.run()


class TestExportSettings:
    """Test suite for ExportSettings."""
