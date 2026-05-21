import importlib

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture()
def client():
    """Return a fresh TestClient with a reloaded app module for each test."""
    importlib.reload(app_module)
    return TestClient(app_module.app)
