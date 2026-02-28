"""
Authentication tests
"""
import pytest
from fastapi import status


class TestAuthRegister:
    """Test user registration"""
    
    def test_register_customer_success(self, client):
        """Test successful customer registration"""
        response = client.post(
            "/auth/register",
            json={
                "email": "newcustomer@test.com",
                "password": "password123",
                "full_name": "New Customer",
                "phone": "+1234567890",
                "role": "customer"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "newcustomer@test.com"
        assert data["full_name"] == "New Customer"
        assert data["role"] == "customer"
        assert "id" in data
    
    def test_register_agent_success(self, client):
        """Test successful agent registration"""
        response = client.post(
            "/auth/register",
            json={
                "email": "newagent@test.com",
                "password": "password123",
                "full_name": "New Agent",
                "role": "agent"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["role"] == "agent"
    
    def test_register_duplicate_email(self, client, test_customer):
        """Test registration with existing email"""
        response = client.post(
            "/auth/register",
            json={
                "email": "customer@test.com",
                "password": "password123",
                "full_name": "Duplicate User"
            }
        )
        assert response.status_code == status.HTTP_409_CONFLICT
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        response = client.post(
            "/auth/register",
            json={
                "email": "invalid-email",
                "password": "password123",
                "full_name": "Test User"
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestAuthLogin:
    """Test user login"""
    
    def test_login_success(self, client, test_customer):
        """Test successful login"""
        response = client.post(
            "/auth/login",
            data={"username": "customer@test.com", "password": "password123"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_json_endpoint(self, client, test_customer):
        """Test login with JSON endpoint"""
        response = client.post(
            "/auth/token",
            json={"email": "customer@test.com", "password": "password123"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
    
    def test_login_invalid_email(self, client):
        """Test login with non-existent email"""
        response = client.post(
            "/auth/login",
            data={"username": "nonexistent@test.com", "password": "password123"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_invalid_password(self, client, test_customer):
        """Test login with wrong password"""
        response = client.post(
            "/auth/login",
            data={"username": "customer@test.com", "password": "wrongpassword"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_inactive_user(self, client, db, test_customer):
        """Test login with inactive user"""
        # Deactivate user
        test_customer.is_active = False
        db.commit()
        
        response = client.post(
            "/auth/login",
            data={"username": "customer@test.com", "password": "password123"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthToken:
    """Test token validation"""
    
    def test_valid_token_access(self, client, customer_token):
        """Test accessing protected route with valid token"""
        response = client.get(
            "/shipments",
            headers={"Authorization": f"Bearer {customer_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_invalid_token_access(self, client):
        """Test accessing protected route with invalid token"""
        response = client.get(
            "/shipments",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_missing_token_access(self, client):
        """Test accessing protected route without token"""
        response = client.get("/shipments")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
