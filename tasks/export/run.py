from logging import getLogger
from typing import TYPE_CHECKING

from tasks.export.settings import ExportSettings

if TYPE_CHECKING:
    from tasks.base import T_co
logger = getLogger(__name__)


class ExportTask:
    """Export Task."""

    def __init__(
        self,
        *args: tuple[T_co],  # noqa: ARG002
        **kwargs: dict[str, T_co],  # noqa: ARG002
    ) -> None:
        """Initialize the Export Task.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        """
        self.settings = ExportSettings()

    def run(self) -> None:
        """Run the Export Task."""
        logger.info("settings=%s", self.settings)
