from logging import getLogger

from tasks.base import T_co
from tasks.evaluation.settings import EvaluationSettings

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
