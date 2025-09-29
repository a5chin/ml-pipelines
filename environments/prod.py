from environments.settings import EnvironmentSettings


def get_env_settings() -> EnvironmentSettings:
    """Get production environment settings."""
    return EnvironmentSettings(
        project_id="your-prod-project-id",
        location="us-central1",
    )
