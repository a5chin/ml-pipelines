from pydantic import BaseModel
from pydantic.types import PositiveInt  # noqa: TC002


class TrainingSettings(BaseModel):
    """Settings for Training Task."""

    seed: PositiveInt = 42
