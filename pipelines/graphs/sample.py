from typing import TYPE_CHECKING

from kfp import dsl

from pipelines.components import (
    evaluation,
    export,
    feature_engineering,
    inference,
    training,
)

if TYPE_CHECKING:
    from kfp.dsl import PipelineTask
    from kfp.dsl.graph_component import GraphComponent

    from pipelines.settings import PipelineCompileArgs


def get_pipeline(args: PipelineCompileArgs) -> GraphComponent:
    """Get sample pipeline.

    Args:
        args (PipelineCompileArgs): Pipeline argments for compilation.

    Returns:
        GraphComponent: Pipeline Graph Component.

    """

    @dsl.pipeline(name=args.pipeline_name)
    def pipeline_def(execution_date: str) -> None:
        feature_engineering_task = feature_engineering(
            image=args.image,
            execution_date=execution_date,
            model_type=args.model_type,
        ).set_display_name("Feature Engineering")

        training_task = (
            training(
                image=args.image,
                execution_date=execution_date,
                model_type=args.model_type,
            )
            .set_retry(
                num_retries=args.num_retries if args.num_retries else 0,
                backoff_duration=args.backoff_duration,
                backoff_factor=args.backoff_factor,
            )
            .after(feature_engineering_task)
            .set_display_name("Train Model")
        )

        inference_task = (
            inference(
                image=args.image,
                execution_date=execution_date,
                model_type=args.model_type,
            )
            .after(training_task)
            .set_display_name("Run Inference")
        )

        evaluation_task = (
            evaluation(
                image=args.image,
                execution_date=execution_date,
                model_type=args.model_type,
            )
            .after(inference_task)
            .set_display_name("Evaluate Model")
        )

        export_task = (
            export(
                image=args.image,
                execution_date=execution_date,
                model_type=args.model_type,
            )
            .after(evaluation_task)
            .set_display_name("Export Features")
        )

        tasks: tuple[PipelineTask, ...] = (
            feature_engineering_task,
            training_task,
            inference_task,
            evaluation_task,
            export_task,
        )
        for task in tasks:
            task.container_spec.image = "{{$.inputs.parameters['image']}}"  # type: ignore[reportOptionalMemberAccess]

    return pipeline_def  # type: ignore[reportReturnType]
