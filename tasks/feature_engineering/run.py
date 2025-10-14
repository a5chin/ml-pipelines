from logging import getLogger
from typing import TYPE_CHECKING

from tasks.feature_engineering.settings import FeatureEngineeringSettings

if TYPE_CHECKING:
    from tasks.base import T_co

logger = getLogger(__name__)


class FeatureEngineeringTask:
    """Feature Engineering Task."""

    def __init__(
        self,
        *args: tuple[T_co],  # noqa: ARG002
        **kwargs: dict[str, T_co],  # noqa: ARG002
    ) -> None:
        """Initialize the Feature Engineering Task.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        """
        self.settings = FeatureEngineeringSettings()

    def run(self) -> None:
        """Run the Feature Engineering Task."""
        logger.info("settings=%s", self.settings)
