from pydantic import BaseModel
from pydantic.types import PositiveInt


class TrainingSettings(BaseModel):
    """Settings for Training Tasks."""

    seed: PositiveInt = 42
