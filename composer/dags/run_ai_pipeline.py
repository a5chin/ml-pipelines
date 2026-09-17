"""Airflow DAG for executing ML pipelines on Vertex AI.

This module defines a DAG that triggers Vertex AI Pipeline Jobs for ML models.
It reads model configurations from JSON files and executes pipelines with
specified parameters.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from airflow.models import BaseOperator
from airflow.providers.google.cloud.operators.vertex_ai.pipeline_job import (
    RunPipelineJobOperator,
)
from airflow.sdk import Param, dag
from airflow.sdk.definitions.param import ParamsDict

if TYPE_CHECKING:
    from airflow.sdk.definitions.context import Context


class ModelPipelineOperator(BaseOperator):
    """Custom operator for executing Vertex AI Pipeline Jobs.

    This operator loads model configuration from a JSON file and triggers
    a Vertex AI Pipeline Job with the specified parameters.
    """

    template_fields = ("model_type", "execution_jst")

    def __init__(
        self,
        model_type: str,
        execution_jst: str,
        *args,  # noqa: ANN002
        **kwargs,  # noqa: ANN003
    ) -> None:
        """Initialize the ModelPipelineOperator.

        Args:
            model_type: Type of the ML model to execute.
            execution_jst: Execution timestamp in JST timezone (ISO format).
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        """
        super().__init__(*args, **kwargs)
        self.model_type = model_type
        self.execution_jst = execution_jst

    def execute(self, context: Context) -> dict[str, Any]:
        """Execute the Vertex AI Pipeline Job.

        Loads model configuration from a JSON file and triggers the pipeline
        with parameters from the DAG context.

        Args:
            context: Airflow task execution context.

        Returns:
            dict[str, Any]: Result from the pipeline job execution.

        Raises:
            FileNotFoundError: If the model configuration file does not exist.

        """
        params = context["params"]
        debug: bool = params["debug"]
        enable_caching: bool = params["enable_caching"]

        config_path = Path(__file__).parent / f"{self.model_type}.json"

        if not config_path.exists():
            msg = f"Config file not found: {config_path.as_posix()}"
            raise FileNotFoundError(msg)

        with config_path.open("r") as f:
            config = json.load(f)

        project_id = config["project_id"]
        env = config["environment"]
        location = config["location"]
        model_type = config["model_type"]
        pipeline_name = f"{env}-{model_type}-pipeline"

        operator = RunPipelineJobOperator(
            task_id=self.task_id,
            project_id=config["project_id"],
            region=location,
            display_name=f"{env}-{model_type}-pipeline",
            template_path=f"https://{location}-kfp.pkg.dev/{project_id}/{pipeline_name}-kfp",
            pipeline_root=f"gs://{project_id}-{pipeline_name}-root",
            parameter_values={
                "model_type": self.model_type,
                "execution_jst": self.execution_jst,
                "debug": debug,
            },
            enable_caching=enable_caching,
            service_account=f"{pipeline_name}-runner@{project_id}.iam.gserviceaccount.com",
        )

        return operator.execute(context)


JST = timezone(timedelta(hours=+9), "JST")

default_args = {"owner": "airflow", "retries": 0}
default_execution_jst = (
    datetime.now(JST)
    .replace(hour=0, minute=0, second=0, microsecond=0)
    .isoformat(timespec="seconds")
)


@dag(
    dag_id="run_ai_pipeline",
    default_args=default_args,
    schedule=None,
    catchup=False,
    render_template_as_native_obj=True,
    params=ParamsDict(
        {
            "model_type": Param(
                default="sample", type="string", description="Model Types"
            ),
            "execution_jst": Param(default=default_execution_jst, type="string"),
            "debug": Param(default=False, type="boolean"),
            "enable_caching": Param(default=True, type="boolean"),
        }
    ),
)
def run_pipeline() -> None:
    """Define the AI pipeline DAG.

    Creates a DAG with a single task that executes a Vertex AI Pipeline Job
    based on the specified model type and execution parameters.
    """
    ModelPipelineOperator(
        task_id="run_pipeline",
        model_type="{{ params.model_type }}",
        execution_jst="{{ params.execution_jst }}",
    )


run_pipeline()
