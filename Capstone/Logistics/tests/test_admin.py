"""
Admin tests
"""
import pytest
from uuid import uuid4
from fastapi import status

from tests.conftest import auth_header


class TestGetUsers:
    """Test admin user management"""
    
    def test_admin_get_all_users(self, client, admin_token, test_customer, test_agent):
        """Test admin getting all users"""
        response = client.get(
            "/admin/users",
            headers=auth_header(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "users" in data
        assert "total" in data
        # At least admin, customer, and agent
        assert data["total"] >= 3
    
    def test_admin_filter_users_by_role(self, client, admin_token, test_customer, test_agent):
        """Test filtering users by role"""
        response = client.get(
            "/admin/users?role=customer",
            headers=auth_header(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(user["role"] == "customer" for user in data["users"])
    
    def test_customer_cannot_get_users(self, client, customer_token):
        """Test that customer cannot access user list"""
        response = client.get(
            "/admin/users",
            headers=auth_header(customer_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_agent_cannot_get_users(self, client, agent_token):
        """Test that agent cannot access user list"""
        response = client.get(
            "/admin/users",
            headers=auth_header(agent_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestGetUserById:
    """Test getting user by ID"""
    
    def test_admin_get_user_by_id(self, client, admin_token, test_customer):
        """Test admin getting user by ID"""
        response = client.get(
            f"/admin/users/{test_customer.id}",
            headers=auth_header(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(test_customer.id)
        assert data["email"] == "customer@test.com"
    
    def test_get_nonexistent_user(self, client, admin_token):
        """Test getting non-existent user"""
        fake_id = str(uuid4())
        response = client.get(
            f"/admin/users/{fake_id}",
            headers=auth_header(admin_token)
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateUser:
    """Test admin user updates"""
    
    def test_admin_update_user(self, client, admin_token, test_customer):
        """Test admin updating a user"""
        response = client.put(
            f"/admin/users/{test_customer.id}",
            headers=auth_header(admin_token),
            json={
                "full_name": "Updated Customer Name",
                "phone": "+9999999999"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["full_name"] == "Updated Customer Name"
        assert data["phone"] == "+9999999999"
    
    def test_admin_deactivate_user(self, client, admin_token, test_customer):
        """Test admin deactivating a user"""
        response = client.put(
            f"/admin/users/{test_customer.id}",
            headers=auth_header(admin_token),
            json={"is_active": False}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_active"] == False


class TestDeleteUser:
    """Test admin user deletion"""
    
    def test_admin_delete_user(self, client, admin_token, test_customer):
        """Test admin deleting a user"""
        response = client.delete(
            f"/admin/users/{test_customer.id}",
            headers=auth_header(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify deletion
        get_response = client.get(
            f"/admin/users/{test_customer.id}",
            headers=auth_header(admin_token)
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


class TestGetAgents:
    """Test getting agents list"""
    
    def test_admin_get_agents(self, client, admin_token, test_agent):
        """Test admin getting agents list"""
        response = client.get(
            "/admin/agents",
            headers=auth_header(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert all(user["role"] == "agent" for user in data)


class TestAdminReports:
    """Test admin reports"""
    
    def test_get_admin_reports(self, client, admin_token, customer_token, test_hub):
        """Test getting admin reports"""
        # Create some shipments
        for i in range(3):
            client.post(
                "/shipments",
                headers=auth_header(customer_token),
                json={
                    "source_address": f"City {i}",
                    "destination_address": f"City {i+1}"
                }
            )
        
        response = client.get(
            "/admin/reports",
            headers=auth_header(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verify required fields
        assert "total_shipments_today" in data
        assert "delivered" in data
        assert "in_transit" in data
        assert "total_users" in data
        assert "total_customers" in data
        assert "total_agents" in data
        assert "total_hubs" in data
    
    def test_customer_cannot_access_reports(self, client, customer_token):
        """Test that customer cannot access reports"""
        response = client.get(
            "/admin/reports",
            headers=auth_header(customer_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_agent_cannot_access_reports(self, client, agent_token):
        """Test that agent cannot access reports"""
        response = client.get(
            "/admin/reports",
            headers=auth_header(agent_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestAdminShipmentManagement:
    """Test admin shipment management"""
    
    def test_admin_view_all_shipments(self, client, admin_token, customer_token):
        """Test admin viewing all shipments"""
        # Create shipment as customer
        client.post(
            "/shipments",
            headers=auth_header(customer_token),
            json={
                "source_address": "Chennai",
                "destination_address": "Bangalore"
            }
        )
        
        # Admin views all shipments
        response = client.get(
            "/shipments",
            headers=auth_header(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["shipments"]) >= 1
