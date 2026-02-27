"""
Authentication Tests - Essential test cases only.
"""

import pytest


class TestAuth:
    """Core authentication tests."""

    def test_register_user(self, client):
        """Test user registration."""
        response = client.post("/auth/register", json={
            "username": "newuser",
            "email": "newuser@test.com",
            "password": "password123",
            "role": "candidate"
        })
        assert response.status_code == 200
        assert response.json()["email"] == "newuser@test.com"

    def test_login_success(self, client, candidate_user):
        """Test successful login."""
        response = client.post("/auth/login", data={
            "username": "candidate@test.com",
            "password": "candidate123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_wrong_password(self, client, candidate_user):
        """Test login with wrong password."""
        response = client.post("/auth/login", data={
            "username": "candidate@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code in [400, 401]

    def test_register_invalid_email(self, client):
        """Test registration with invalid email."""
        response = client.post("/auth/register", json={
            "username": "user",
            "email": "invalid",
            "password": "pass",
            "role": "candidate"
        })
        assert response.status_code == 422
