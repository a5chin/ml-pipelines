import tempfile
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING

from kfp import compiler
from kfp.registry import RegistryClient

from const import ModelType
from pipelines.graphs import sample
from pipelines.settings import CLIArgs, PipelineCompileArgs

if TYPE_CHECKING:
    from collections.abc import Callable

    from kfp.dsl.graph_component import GraphComponent

logger = getLogger(__name__)

pipeline_types = {
    ModelType.SAMPLE: sample.get_pipeline,
}


def compile_and_upload_pipeline(
    pipeline_func: Callable[[PipelineCompileArgs], GraphComponent],
    args: PipelineCompileArgs,
) -> None:
    """Compile and upload the pipeline.

    Args:
        pipeline_func (Callable[[PipelineCompileArgs], GraphComponent]):
            Pipeline function.
        args (PipelineCompileArgs): Arguments for pipeline compilation.

    """
    logger.info("args=%s", args)

    with tempfile.TemporaryDirectory() as td:
        package_path = (Path(td) / f"{args.pipeline_name}.yaml").as_posix()

        compiler.Compiler().compile(
            pipeline_func=pipeline_func(args),
            package_path=package_path,
        )

        client = RegistryClient(host=args.pipeline_template_host)
        template_name, version = client.upload_pipeline(
            file_name=package_path,
            tags=[args.tag],
            extra_headers={"description": f"Pipeline for {args.model_type} model"},
        )

        logger.info(
            "Uploaded pipeline to %s/%s/%s",
            args.pipeline_template_host,
            template_name,
            version,
        )


def main() -> None:
    """Compile the pipeline."""
    cli_args = CLIArgs()  # type: ignore[reportCallIssue]
    args = PipelineCompileArgs.build(
        env=cli_args.env,
        pipeline_name=cli_args.pipeline_name,
        tag=cli_args.tag,
        model_type=cli_args.model_type,
    )

    pipeline_func = pipeline_types[cli_args.model_type]

    compile_and_upload_pipeline(pipeline_func, args)


if __name__ == "__main__":  # pragma: no cover
    main()
