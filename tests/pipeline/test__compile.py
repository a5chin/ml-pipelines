import pytest
from kfp.dsl.graph_component import GraphComponent

from const import Environment, ModelType
from pipelines.main import pipeline_types
from pipelines.settings import PipelineCompileArgs


class TestCompilePipeline:
    """Test suite for Compile Pipeline."""

    @pytest.mark.parametrize(
        (
            "env",
            "pipeline_name",
            "tag",
            "model_type",
        ),
        [
            (
                Environment.DEV,
                "pipeline-name",
                "v1.0",
                ModelType.SAMPLE,
            ),
        ],
    )
    def test_pipeline_compile_args(
        self,
        env: Environment,
        pipeline_name: str,
        tag: str,
        model_type: ModelType,
    ) -> None:
        """Test Compile Pipeline."""
        args = PipelineCompileArgs.build(
            env=env,
            pipeline_name=pipeline_name,
            tag=tag,
            model_type=model_type,
        )
        component = pipeline_types[model_type](args)

        if not isinstance(component, GraphComponent):
            pytest.fail(f"Expected GraphComponent, got {type(component)}")
