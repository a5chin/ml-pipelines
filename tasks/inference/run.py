from logging import getLogger

from tasks.base import T_co  # noqa: TC001
from tasks.inference.settings import InferenceSettings

logger = getLogger(__name__)


class InferenceTask:
    """Inference Task."""

    def __init__(
        self,
        *args: tuple[T_co],  # noqa: ARG002
        **kwargs: dict[str, T_co],  # noqa: ARG002
    ) -> None:
        """Initialize the Inference Task.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        """
        self.settings = InferenceSettings()

    def run(self) -> None:
        """Run the Inference Task."""
        logger.info("settings=%s", self.settings)
