import importlib
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from const import Environments


class EnvironmentSettings(BaseModel):
    """Environment settings."""

    project_id: str
    location: str


def load_env_settings(env: Environments) -> EnvironmentSettings:
    """Load environment settings."""
    module = importlib.import_module(f"environments.{env}")
    return module.get_env_settings()
