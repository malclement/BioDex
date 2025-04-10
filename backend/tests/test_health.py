import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_endpoint():
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "mongodb" in data
