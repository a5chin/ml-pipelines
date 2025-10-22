"""Conftest for pipeline."""

from unittest.mock import MagicMock

import pytest
from kfp.registry import RegistryClient


@pytest.fixture
def registry_client() -> RegistryClient:
    """Fixture for RegistryClient."""
    registry_client: RegistryClient = MagicMock(spec=RegistryClient)
    registry_client.upload_pipeline.return_value = ("template_name", "version")
    return registry_client
