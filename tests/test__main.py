import sys
from typing import TYPE_CHECKING

import pytest

import main
from const import Environments, ModelTypes, Tasks
from tasks import (
    EvaluationTask,
    ExportTask,
    FeatureEngineeringTask,
    InferenceTask,
    TrainingTask,
)

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestMain:
    """Test suite for CLIArgs using mocked sys.argv."""

    @pytest.mark.parametrize(
        ("env", "model_type"),
        [
            (Environments.DEV, ModelTypes.SAMPLE),
            (Environments.PROD, ModelTypes.SAMPLE),
        ],
    )
    def test_feature_engineering(
        self,
        mocker: MockerFixture,
        env: Environments,
        model_type: ModelTypes,
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
                Tasks.FEATUREENGINEERING,
            ],
        )
        mock_run = mocker.patch.object(FeatureEngineeringTask, "run", return_value=None)

        main.main()

        mock_run.assert_called_once()

    @pytest.mark.parametrize(
        ("env", "model_type"),
        [
            (Environments.DEV, ModelTypes.SAMPLE),
            (Environments.PROD, ModelTypes.SAMPLE),
        ],
    )
    def test_training(
        self,
        mocker: MockerFixture,
        env: Environments,
        model_type: ModelTypes,
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
                Tasks.TRAING,
            ],
        )
        mock_run = mocker.patch.object(TrainingTask, "run", return_value=None)

        main.main()

        mock_run.assert_called_once()

    @pytest.mark.parametrize(
        ("env", "model_type"),
        [
            (Environments.DEV, ModelTypes.SAMPLE),
            (Environments.PROD, ModelTypes.SAMPLE),
        ],
    )
    def test_inference(
        self,
        mocker: MockerFixture,
        env: Environments,
        model_type: ModelTypes,
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
                Tasks.INFERENCE,
            ],
        )
        mock_run = mocker.patch.object(InferenceTask, "run", return_value=None)

        main.main()

        mock_run.assert_called_once()

    @pytest.mark.parametrize(
        ("env", "model_type"),
        [
            (Environments.DEV, ModelTypes.SAMPLE),
            (Environments.PROD, ModelTypes.SAMPLE),
        ],
    )
    def test_evaluation(
        self,
        mocker: MockerFixture,
        env: Environments,
        model_type: ModelTypes,
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
                Tasks.EVALUATION,
            ],
        )
        mock_run = mocker.patch.object(EvaluationTask, "run", return_value=None)

        main.main()

        mock_run.assert_called_once()

    @pytest.mark.parametrize(
        ("env", "model_type"),
        [
            (Environments.DEV, ModelTypes.SAMPLE),
            (Environments.PROD, ModelTypes.SAMPLE),
        ],
    )
    def test_export(
        self,
        mocker: MockerFixture,
        env: Environments,
        model_type: ModelTypes,
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
                Tasks.EXPORT,
            ],
        )
        mock_run = mocker.patch.object(ExportTask, "run", return_value=None)

        main.main()

        mock_run.assert_called_once()
