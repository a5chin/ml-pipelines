import json
from pathlib import Path
from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock, mock_open

if TYPE_CHECKING:
    from airflow.sdk.definitions.context import Context
import pytest

from composer.dags.run_ai_pipeline import ModelPipelineOperator

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestModelPipelineOperator:
    """Test suite for ModelPipelineOperator."""

    @pytest.mark.parametrize(
        ("model_type", "execution_jst", "task_id"),
        [
            ("sample", "2026-01-01T00:00:00+09:00", "run_pipeline"),
        ],
    )
    def test_init(
        self,
        model_type: str,
        execution_jst: str,
        task_id: str,
    ) -> None:
        """Test ModelPipelineOperator initialization."""
        operator = ModelPipelineOperator(
            task_id=task_id,
            model_type=model_type,
            execution_jst=execution_jst,
        )

        assert operator.task_id == task_id
        assert operator.model_type == model_type
        assert operator.execution_jst == execution_jst
        assert "model_type" in operator.template_fields
        assert "execution_jst" in operator.template_fields

    @pytest.mark.parametrize(
        (
            "model_type",
            "execution_jst",
            "debug",
            "enable_caching",
            "config",
        ),
        [
            (
                "sample",
                "2026-06-10T00:00:00+09:00",
                False,
                True,
                {
                    "project_id": "your-dev-project-id",
                    "location": "us-central1",
                    "environment": "dev",
                    "model_type": "sample",
                    "pipeline_root": "gs://your-dev-project-id-dev-sample-pipeline-root",
                },
            )
        ],
    )
    def test_execute_success(
        self,
        mocker: MockerFixture,
        model_type: str,
        execution_jst: str,
        debug: bool,
        enable_caching: bool,
        config: dict[str, Any],
    ) -> None:
        """Test ModelPipelineOperator.execute() with valid config."""
        config_json = json.dumps(config)
        mocker.patch("pathlib.Path.open", mock_open(read_data=config_json))
        mocker.patch.object(Path, "exists", return_value=True)

        mock_run_pipeline = mocker.patch(
            "composer.dags.run_ai_pipeline.RunPipelineJobOperator"
        )
        mock_operator_instance = MagicMock()
        mock_operator_instance.execute.return_value = {"job_id": "test-job-123"}
        mock_run_pipeline.return_value = mock_operator_instance

        operator = ModelPipelineOperator(
            task_id="test_task",
            model_type=model_type,
            execution_jst=execution_jst,
        )

        context: Context = {
            "params": {
                "debug": debug,
                "enable_caching": enable_caching,
            }
        }

        result = operator.execute(context)

        assert result == {"job_id": "test-job-123"}

        project_id = config["project_id"]
        env = config["environment"]
        location = config["location"]
        model_type = config["model_type"]
        pipeline_name = f"{env}-{model_type}-pipeline"

        mock_run_pipeline.assert_called_once_with(
            task_id="test_task",
            project_id=config["project_id"],
            region=location,
            display_name=f"{env}-{model_type}-pipeline",
            template_path=f"https://{location}-kfp.pkg.dev/{project_id}/{pipeline_name}-kfp",
            pipeline_root=f"gs://{project_id}-{pipeline_name}-root",
            parameter_values={
                "model_type": model_type,
                "execution_jst": execution_jst,
                "debug": debug,
            },
            enable_caching=enable_caching,
            service_account=f"{pipeline_name}-runner@{project_id}.iam.gserviceaccount.com",
        )

    @pytest.mark.parametrize(
        ("model_type", "execution_jst"),
        [
            ("sample", "2026-01-01T00:00:00+09:00"),
        ],
    )
    def test_execute_config_not_found(
        self,
        mocker: MockerFixture,
        model_type: str,
        execution_jst: str,
    ) -> None:
        """Test ModelPipelineOperator.execute() raises FileNotFoundError."""
        mocker.patch.object(Path, "exists", return_value=False)

        operator = ModelPipelineOperator(
            task_id="test_task",
            model_type=model_type,
            execution_jst=execution_jst,
        )

        context: Context = {
            "params": {
                "debug": False,
                "enable_caching": True,
            }
        }

        with pytest.raises(FileNotFoundError):
            operator.execute(context)
