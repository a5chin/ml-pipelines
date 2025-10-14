from logging import getLogger
from typing import TYPE_CHECKING

from tasks.evaluation.settings import EvaluationSettings

if TYPE_CHECKING:
    from tasks.base import T_co

logger = getLogger(__name__)


class EvaluationTask:
    """Evaluation Task."""

    def __init__(
        self,
        *args: tuple[T_co],  # noqa: ARG002
        **kwargs: dict[str, T_co],  # noqa: ARG002
    ) -> None:
        """Initialize the Evaluation Task.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        """
        self.settings = EvaluationSettings()

    def run(self) -> None:
        """Run the Evaluation Task."""
        logger.info("settings=%s", self.settings)
