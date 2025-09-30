import pytest

from const import ModelTypes


class TestModelTypes:
    """Test suite for the ModelTypes."""

    @pytest.mark.parametrize(
        ("model_type", "expected"),
        [
            (ModelTypes.SAMPLE, "sample"),
        ],
    )
    def test_all(self, model_type: ModelTypes, expected: str) -> None:
        """Test All Model Types."""
        if model_type != expected:
            pytest.fail(f"Expected '{expected}', but got '{model_type}'")
