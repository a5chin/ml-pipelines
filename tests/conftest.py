"""Conftest for tests."""

from unittest.mock import MagicMock

import pytest


@pytest.fixture
def registry_client() -> MagicMock:
    """Fixture for RegistryClient."""
    registry_client = MagicMock()
    registry_client.upload_pipeline.return_value = ("template_name", "version")
    return registry_client
