from logging import getLogger
from typing import TYPE_CHECKING

from tasks.training.settings import TrainingSettings

if TYPE_CHECKING:
    from tasks.base import T_co

logger = getLogger(__name__)


class TrainingTask:
    """Training Task."""

    def __init__(
        self,
        *args: tuple[T_co],  # noqa: ARG002
        **kwargs: dict[str, T_co],  # noqa: ARG002
    ) -> None:
        """Initialize the Training Task.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        """
        self.settings = TrainingSettings()

    def run(self) -> None:
        """Run the Training Task."""
        logger.info("settings=%s", self.settings)
