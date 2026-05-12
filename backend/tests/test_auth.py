import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_login_success():
    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 300


def test_login_wrong_password():
    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_unknown_user():
    response = client.post(
        "/auth/token",
        json={"username": "unknown", "password": "admin123"},
    )
    assert response.status_code == 401


def test_refresh_token_success():
    # First obtain a token pair
    login_response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "admin123"},
    )
    refresh_token = login_response.json()["refresh_token"]

    # Use the refresh token to get a new pair
    response = client.post(
        "/auth/token/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["expires_in"] == 300


def test_refresh_token_invalid():
    response = client.post(
        "/auth/token/refresh",
        json={"refresh_token": "not.a.valid.token"},
    )
    assert response.status_code == 401


def test_refresh_token_using_access_token_fails():
    """Access tokens must not be accepted as refresh tokens."""
    login_response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "admin123"},
    )
    access_token = login_response.json()["access_token"]

    response = client.post(
        "/auth/token/refresh",
        json={"refresh_token": access_token},
    )
    assert response.status_code == 401
