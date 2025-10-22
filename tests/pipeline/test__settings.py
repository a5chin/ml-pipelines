import pytest

from const import Environment, ModelType
from pipelines.settings import CLIArgs, PipelineCompileArgs


class TestArgs:
    """Test suite for CLIArgs and  CLIArgs."""

    @pytest.mark.parametrize(
        ("env", "pipeline_name", "tag", "model_type", "error"),
        [
            (Environment.DEV, "sample-pipeline", "v1.1", ModelType.SAMPLE, None),
            (Environment.PROD, "sample-pipeline", "v1.0", ModelType.SAMPLE, None),
            ("qa", "sample-pipeline", "v1.0", ModelType.SAMPLE, ValueError),
            (Environment.DEV, "sample-pipeline", 1.0, ModelType.SAMPLE, ValueError),
            (
                Environment.PROD,
                "sample-pipeline",
                "v1.0",
                "example-pipeline",
                ValueError,
            ),
        ],
    )
    def test_cli_args(
        self,
        env: Environment,
        pipeline_name: str,
        tag: str,
        model_type: ModelType,
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
            _ = CLIArgs(
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
                Environment.DEV,
                "pipeline-name",
                "v1.0",
                ModelType.SAMPLE,
                PipelineCompileArgs(
                    project_id="your-dev-project-id",
                    location="us-central1",
                    pipeline_name="dev-pipeline-name",
                    image="us-central1-docker.pkg.dev/your-dev-project-id/pipeline-name-docker/runner:v1.0",
                    pipeline_template_host="https://us-central1-kfp.pkg.dev/your-dev-project-id/pipeline-name-kfp",
                    tag="v1.0",
                    model_type=ModelType.SAMPLE,
                ),
            ),
        ],
    )
    def test_pipeline_compile_args(
        self,
        env: Environment,
        pipeline_name: str,
        tag: str,
        model_type: ModelType,
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
