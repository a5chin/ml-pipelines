import pytest

from const import Environments
from environments.settings import EnvironmentSettings, load_env_settings


class TestEnvironments:
    """Test suite for the Environments."""

    @pytest.mark.parametrize(
        ("env", "expected"),
        [
            (Environments.DEV, "dev"),
            (Environments.PROD, "prod"),
        ],
    )
    def test_const(self, env: Environments, expected: str) -> None:
        """Test All Environments."""
        if env != expected:
            pytest.fail(f"Expected '{expected}', but got '{env}'")

    @pytest.mark.parametrize(
        ("env", "expected"),
        [
            (
                Environments.DEV,
                EnvironmentSettings(
                    project_id="your-dev-project-id", location="us-central1"
                ),
            ),
            (
                Environments.PROD,
                EnvironmentSettings(
                    project_id="your-prod-project-id", location="us-central1"
                ),
            ),
        ],
    )
    def test_load_env_settings(
        self, env: Environments, expected: EnvironmentSettings
    ) -> None:
        """Test load_env_settings function."""
        settings = load_env_settings(env)
        if settings != expected:
            pytest.fail(f"Expected '{expected}', but got '{settings}'")
