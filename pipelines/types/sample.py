from __future__ import annotations

from typing import cast

from kfp import dsl
from kfp.dsl import base_component  # noqa: TC002

from pipelines.components import (
    evaluation,
    export,
    feature_engineering,
    inference,
    training,
)
from pipelines.settings import PipelineCompileArgs  # noqa: TC001


def get_pipeline(args: PipelineCompileArgs) -> base_component.BaseComponent:
    """Get sample pipeline.

    Args:
        args (PipelineCompileArgs): Pipeline argments for compilation.

    Returns:
        base_component.BaseComponent: Pipeline function.

    """

    @dsl.pipeline(name=args.pipeline_name)
    def pipeline_def() -> None:
        feature_engineering_task = feature_engineering(
            image=args.image,
            model_type=args.model_type,
        ).set_display_name("Feature Engineering")

        training_task = (
            training(
                image=args.image,
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
                model_type=args.model_type,
            )
            .after(training_task)
            .set_display_name("Run Inference")
        )

        evaluation_task = (
            evaluation(
                image=args.image,
                model_type=args.model_type,
            )
            .after(inference_task)
            .set_display_name("Evaluate Model")
        )

        export(
            image=args.image,
            model_type=args.model_type,
        ).after(evaluation_task).set_display_name("Export Features")

    return cast("base_component.BaseComponent", pipeline_def)
