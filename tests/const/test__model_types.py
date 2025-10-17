import pytest

from const import ModelType


class TestModelType:
    """Test suite for the ModelType."""

    @pytest.mark.parametrize(
        ("model_type", "expected"),
        [
            (ModelType.SAMPLE, "sample"),
        ],
    )
    def test_all(self, model_type: ModelType, expected: str) -> None:
        """Test All Model Types."""
        if model_type != expected:
            pytest.fail(f"Expected '{expected}', but got '{model_type}'")
