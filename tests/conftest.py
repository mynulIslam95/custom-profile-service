from src.app import app, reset_store, set_ready

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    reset_store()
    set_ready(True)
    return TestClient(app)
