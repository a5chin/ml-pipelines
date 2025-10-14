from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from pydantic.types import PositiveInt


class TrainingSettings(BaseModel):
    """Settings for Training Tasks."""

    seed: PositiveInt = 42
