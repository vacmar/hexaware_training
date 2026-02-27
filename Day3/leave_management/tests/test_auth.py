"""
Authentication Tests for Leave Management System.
"""

import pytest


class TestAuth:
    """Core authentication tests."""

    def test_register_user(self, client):
        """Test user registration."""
        response = client.post("/auth/register", json={
            "name": "New User",
            "email": "newuser@test.com",
            "password": "password123",
            "role": "EMPLOYEE"
        })
        assert response.status_code == 200
        assert response.json()["email"] == "newuser@test.com"
        assert response.json()["role"] == "EMPLOYEE"

    def test_register_admin(self, client):
        """Test admin registration."""
        response = client.post("/auth/register", json={
            "name": "Admin User",
            "email": "admin@test.com",
            "password": "admin123",
            "role": "ADMIN"
        })
        assert response.status_code == 200
        assert response.json()["role"] == "ADMIN"

    def test_register_manager(self, client):
        """Test manager registration."""
        response = client.post("/auth/register", json={
            "name": "Manager User",
            "email": "manager@test.com",
            "password": "manager123",
            "role": "MANAGER"
        })
        assert response.status_code == 200
        assert response.json()["role"] == "MANAGER"

    def test_register_duplicate_email(self, client, employee_user):
        """Test registration with existing email."""
        response = client.post("/auth/register", json={
            "name": "Another User",
            "email": "employee@test.com",
            "password": "password123",
            "role": "EMPLOYEE"
        })
        assert response.status_code == 400

    def test_register_invalid_role(self, client):
        """Test registration with invalid role."""
        response = client.post("/auth/register", json={
            "name": "Invalid User",
            "email": "invalid@test.com",
            "password": "password123",
            "role": "INVALID_ROLE"
        })
        assert response.status_code == 400

    def test_login_success(self, client, employee_user):
        """Test successful login."""
        response = client.post("/auth/login", data={
            "username": "employee@test.com",
            "password": "employee123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_wrong_password(self, client, employee_user):
        """Test login with wrong password."""
        response = client.post("/auth/login", data={
            "username": "employee@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_login_invalid_email(self, client):
        """Test login with non-existent email."""
        response = client.post("/auth/login", data={
            "username": "nonexistent@test.com",
            "password": "password123"
        })
        assert response.status_code == 401

    def test_register_invalid_email_format(self, client):
        """Test registration with invalid email format."""
        response = client.post("/auth/register", json={
            "name": "User",
            "email": "invalid-email",
            "password": "pass123",
            "role": "EMPLOYEE"
        })
        assert response.status_code == 422
