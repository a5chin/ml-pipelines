from typing import TYPE_CHECKING

from pydantic import BaseModel, PositiveFloat, PositiveInt
from pydantic_settings import BaseSettings

from environments.settings import load_env_settings

if TYPE_CHECKING:
    from const import Environments, ModelTypes


class CLIArgs(BaseSettings):
    """CLI Arguments."""

    env: Environments
    pipeline_name: str
    tag: str
    model_type: ModelTypes


class PipelineCompileArgs(BaseModel):
    """Pipeline Compile Arguments."""

    project_id: str
    location: str
    pipeline_name: str
    image: str
    pipeline_template_host: str
    tag: str = "latest"
    model_type: ModelTypes
    num_retries: PositiveInt = 3
    backoff_duration: str = "60s"
    backoff_factor: PositiveFloat = 2.0

    @classmethod
    def build(
        cls, env: Environments, pipeline_name: str, tag: str, model_type: ModelTypes
    ) -> PipelineCompileArgs:
        """Args for building PipelineCompileArgs.

        Args:
            env (Environments): Environment
            pipeline_name (str): Pipeline name
            tag (str): Tag for the image
            model_type (ModelTypes): Model type

        Returns:
            PipelineCompileArgs: PipelineCompileArgs

        """
        env_settings = load_env_settings(env)

        return cls(
            project_id=env_settings.project_id,
            location=env_settings.location,
            tag=tag,
            pipeline_name=f"{env}-{pipeline_name}",
            image=f"{env_settings.location}-docker.pkg.dev/{env_settings.project_id}/{pipeline_name}-docker/runner:{tag}",
            pipeline_template_host=f"https://{env_settings.location}-kfp.pkg.dev/{env_settings.project_id}/{pipeline_name}-kfp",
            model_type=model_type,
        )
