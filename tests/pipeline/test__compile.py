import sys
from typing import TYPE_CHECKING

import pytest

from const import Environment, ModelType
from pipelines import main

if TYPE_CHECKING:
    from unittest.mock import MagicMock

    from pytest_mock import MockerFixture


class TestCompilePipeline:
    """Test suite for Compile Pipeline."""

    @pytest.mark.usefixtures("registry_client")
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
            (
                Environment.PROD,
                "pipeline-name",
                "v1.0",
                ModelType.SAMPLE,
            ),
        ],
    )
    def test_compile_pipeline(  # noqa: PLR0913
        self,
        mocker: MockerFixture,
        registry_client: MagicMock,
        env: Environment,
        pipeline_name: str,
        tag: str,
        model_type: ModelType,
    ) -> None:
        """Test Compile Pipeline."""
        mocker.patch.object(
            sys,
            "argv",
            [
                "pipelines.main",
                "--env",
                env,
                "--pipeline_name",
                pipeline_name,
                "--tag",
                tag,
                "--model_type",
                model_type,
            ],
        )
        mocker.patch(
            "pipelines.main.RegistryClient",
            return_value=registry_client,
        )

        main.main()
