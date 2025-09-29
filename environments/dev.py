from environments.settings import EnvironmentSettings


def get_env_settings() -> EnvironmentSettings:
    """Get development environment settings."""
    return EnvironmentSettings(
        project_id="your-dev-project-id",
        location="us-central1",
    )
