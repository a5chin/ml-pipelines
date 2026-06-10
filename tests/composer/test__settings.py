import pytest

from composer import ComposerSettings
from const import ModelType


class TestComposerSettings:
    """Test suite for the Environments."""

    @pytest.mark.parametrize(
        ("project_id", "location", "environment", "tag", "model_type", "error"),
        [
            (
                "project_id",
                "location",
                "environment",
                "v1.0.0",
                ModelType.SAMPLE,
                None,
            ),
            (
                "project_id",
                "location",
                "environment",
                "v1.0.0",
                "example-pipeline",
                ValueError,
            ),
        ],
    )
    def test_composer_settings(
        self,
        project_id: str,
        location: str,
        environment: str,
        tag: str,
        model_type: ModelType,
        error: type[BaseException],
    ) -> None:
        """Test ComposerSettings."""
        if not error:
            _ = ComposerSettings(
                project_id=project_id,
                location=location,
                environment=environment,
                tag=tag,
                model_type=model_type,
            )
            return

        with pytest.raises(error):
            _ = ComposerSettings(
                project_id=project_id,
                location=location,
                environment=environment,
                tag=tag,
                model_type=model_type,
            )
