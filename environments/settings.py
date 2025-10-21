import importlib

from pydantic import BaseModel

from const import Environment  # noqa: TC001


class EnvironmentSettings(BaseModel):
    """Environment settings."""

    project_id: str
    location: str


def load_env_settings(env: Environment) -> EnvironmentSettings:
    """Load environment settings."""
    module = importlib.import_module(f"environments.{env}")
    return module.get_env_settings()
