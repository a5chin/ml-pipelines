from pydantic import BaseModel
from pydantic.types import PositiveInt  # noqa: TC002


class TrainingSettings(BaseModel):
    """Settings for Training Tasks."""

    seed: PositiveInt = 42
