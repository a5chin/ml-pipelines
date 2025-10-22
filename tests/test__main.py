import sys

import pytest
from pytest_mock import MockerFixture  # noqa: TC002

import main
from const import Environment, ModelType, Task
from tasks import (
    EvaluationTask,
    ExportTask,
    FeatureEngineeringTask,
    InferenceTask,
    TrainingTask,
)


class TestMain:
    """Test suite for CLIArgs using mocked sys.argv."""

    @pytest.mark.parametrize(
        ("env", "model_type"),
        [
            (Environment.DEV, ModelType.SAMPLE),
            (Environment.PROD, ModelType.SAMPLE),
        ],
    )
    def test_feature_engineering(
        self,
        mocker: MockerFixture,
        env: Environment,
        model_type: ModelType,
    ) -> None:
        """Test CLIArgs parses sys.argv and executes FeatureEngineeringTask.run()."""
        mocker.patch.object(
            sys,
            "argv",
            [
                "main.py",
                "--env",
                env,
                "--model_type",
                model_type,
                "--task",
                Task.FEATURE_ENGINEERING,
            ],
        )
        mock_run = mocker.patch.object(FeatureEngineeringTask, "run", return_value=None)

        main.main()

        mock_run.assert_called_once()

    @pytest.mark.parametrize(
        ("env", "model_type"),
        [
            (Environment.DEV, ModelType.SAMPLE),
            (Environment.PROD, ModelType.SAMPLE),
        ],
    )
    def test_training(
        self,
        mocker: MockerFixture,
        env: Environment,
        model_type: ModelType,
    ) -> None:
        """Test CLIArgs parses sys.argv and executes Training.run()."""
        mocker.patch.object(
            sys,
            "argv",
            [
                "main.py",
                "--env",
                env,
                "--model_type",
                model_type,
                "--task",
                Task.TRAINING,
            ],
        )
        mock_run = mocker.patch.object(TrainingTask, "run", return_value=None)

        main.main()

        mock_run.assert_called_once()

    @pytest.mark.parametrize(
        ("env", "model_type"),
        [
            (Environment.DEV, ModelType.SAMPLE),
            (Environment.PROD, ModelType.SAMPLE),
        ],
    )
    def test_inference(
        self,
        mocker: MockerFixture,
        env: Environment,
        model_type: ModelType,
    ) -> None:
        """Test CLIArgs parses sys.argv and executes Inference.run()."""
        mocker.patch.object(
            sys,
            "argv",
            [
                "main.py",
                "--env",
                env,
                "--model_type",
                model_type,
                "--task",
                Task.INFERENCE,
            ],
        )
        mock_run = mocker.patch.object(InferenceTask, "run", return_value=None)

        main.main()

        mock_run.assert_called_once()

    @pytest.mark.parametrize(
        ("env", "model_type"),
        [
            (Environment.DEV, ModelType.SAMPLE),
            (Environment.PROD, ModelType.SAMPLE),
        ],
    )
    def test_evaluation(
        self,
        mocker: MockerFixture,
        env: Environment,
        model_type: ModelType,
    ) -> None:
        """Test CLIArgs parses sys.argv and executes Evaluation.run()."""
        mocker.patch.object(
            sys,
            "argv",
            [
                "main.py",
                "--env",
                env,
                "--model_type",
                model_type,
                "--task",
                Task.EVALUATION,
            ],
        )
        mock_run = mocker.patch.object(EvaluationTask, "run", return_value=None)

        main.main()

        mock_run.assert_called_once()

    @pytest.mark.parametrize(
        ("env", "model_type"),
        [
            (Environment.DEV, ModelType.SAMPLE),
            (Environment.PROD, ModelType.SAMPLE),
        ],
    )
    def test_export(
        self,
        mocker: MockerFixture,
        env: Environment,
        model_type: ModelType,
    ) -> None:
        """Test CLIArgs parses sys.argv and executes Export.run()."""
        mocker.patch.object(
            sys,
            "argv",
            [
                "main.py",
                "--env",
                env,
                "--model_type",
                model_type,
                "--task",
                Task.EXPORT,
            ],
        )
        mock_run = mocker.patch.object(ExportTask, "run", return_value=None)

        main.main()

        mock_run.assert_called_once()
