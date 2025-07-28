import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test that the API is running"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "message": "Watchlist Manager API is running"}

def test_api_docs():
    """Test that API documentation is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_root_endpoint():
    """Test that root endpoint works"""
    response = client.get("/")
    assert response.status_code == 200
