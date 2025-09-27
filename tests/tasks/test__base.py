import pytest

from tasks import BaseTask


class TestBaseTask:
    """Test suite for the BaseTask."""

    def setup_method(self) -> None:
        """Set up BaseTask."""
        self.task = BaseTask()  # type:ignore[reportAbstractUsage]

    def test_not_implemented_error(self) -> None:
        """Test that BaseTask."""
        with pytest.raises(NotImplementedError):
            self.task.run()
