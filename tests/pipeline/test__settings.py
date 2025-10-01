import pytest

from const import Environments, ModelTypes
from pipelines.settings import CLIArgs, PipelineCompileArgs


class TestArgs:
    """Test suite for CLIArgs and  CLIArgs."""

    @pytest.mark.parametrize(
        ("env", "pipeline_name", "tag", "model_type", "error"),
        [
            (Environments.DEV, "sample-pipeline", "v1.1", ModelTypes.SAMPLE, None),
            (Environments.PROD, "sample-pipeline", "v1.0", ModelTypes.SAMPLE, None),
            ("qa", "sample-pipeline", "v1.0", ModelTypes.SAMPLE, ValueError),
            (Environments.DEV, "sample-pipeline", 1.0, ModelTypes.SAMPLE, ValueError),
            (
                Environments.PROD,
                "sample-pipeline",
                "v1.0",
                "example-pipeline",
                ValueError,
            ),
        ],
    )
    def test_cli_args(
        self,
        env: Environments,
        pipeline_name: str,
        tag: str,
        model_type: ModelTypes,
        error: type,
    ) -> None:
        """Test CLIArgs attribute (valid and invalid cases)."""
        if not error:
            _ = CLIArgs(
                env=env,
                pipeline_name=pipeline_name,
                tag=tag,
                model_type=model_type,
            )
            return

        with pytest.raises(error):
            CLIArgs(
                env=env,
                pipeline_name=pipeline_name,
                tag=tag,
                model_type=model_type,
            )

    @pytest.mark.parametrize(
        (
            "env",
            "pipeline_name",
            "tag",
            "model_type",
            "expected",
        ),
        [
            (
                Environments.DEV,
                "pipeline-name",
                "v1.0",
                ModelTypes.SAMPLE,
                PipelineCompileArgs(
                    project_id="your-dev-project-id",
                    location="us-central1",
                    pipeline_name="dev-pipeline-name",
                    image="us-central1-docker.pkg.dev/your-dev-project-id/pipeline-name-docker/runner:v1.0",
                    pipeline_template_host="https://us-central1-kfp.pkg.dev/your-dev-project-id/pipeline-name-kfp",
                    tag="v1.0",
                    model_type=ModelTypes.SAMPLE,
                ),
            ),
        ],
    )
    def test_pipeline_compile_args(
        self,
        env: Environments,
        pipeline_name: str,
        tag: str,
        model_type: ModelTypes,
        expected: PipelineCompileArgs,
    ) -> None:
        """Test PipelineCompileArgs attribute (valid and invalid cases)."""
        args = PipelineCompileArgs.build(
            env=env,
            pipeline_name=pipeline_name,
            tag=tag,
            model_type=model_type,
        )

        if args != expected:
            pytest.fail(f"Expected {expected}, but got {args}")
