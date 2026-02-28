"""
Hub tests
"""
import pytest
from uuid import uuid4
from fastapi import status

from tests.conftest import auth_header


class TestCreateHub:
    """Test hub creation"""
    
    def test_admin_create_hub(self, client, admin_token):
        """Test admin creating a hub"""
        response = client.post(
            "/hubs",
            headers=auth_header(admin_token),
            json={
                "hub_name": "Mumbai Central Hub",
                "city": "Mumbai",
                "address": "123 Commercial Area, Mumbai",
                "contact_phone": "+91-22-12345678",
                "contact_email": "mumbai@logistics.com",
                "capacity": 1500
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["hub_name"] == "Mumbai Central Hub"
        assert data["city"] == "Mumbai"
        assert data["is_active"] == True
    
    def test_agent_cannot_create_hub(self, client, agent_token):
        """Test that agent cannot create a hub"""
        response = client.post(
            "/hubs",
            headers=auth_header(agent_token),
            json={
                "hub_name": "Test Hub",
                "city": "Test City"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_customer_cannot_create_hub(self, client, customer_token):
        """Test that customer cannot create a hub"""
        response = client.post(
            "/hubs",
            headers=auth_header(customer_token),
            json={
                "hub_name": "Test Hub",
                "city": "Test City"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_duplicate_hub_name(self, client, admin_token, test_hub):
        """Test creating hub with duplicate name"""
        response = client.post(
            "/hubs",
            headers=auth_header(admin_token),
            json={
                "hub_name": "Chennai Central Hub",  # Same as test_hub
                "city": "Chennai"
            }
        )
        assert response.status_code == status.HTTP_409_CONFLICT


class TestGetHubs:
    """Test getting hubs"""
    
    def test_get_all_hubs(self, client, test_hub):
        """Test getting all hubs (public)"""
        response = client.get("/hubs")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "hubs" in data
        assert len(data["hubs"]) >= 1
    
    def test_get_hubs_by_city(self, client, test_hub):
        """Test filtering hubs by city"""
        response = client.get("/hubs?city=Chennai")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(hub["city"] == "Chennai" for hub in data["hubs"])
    
    def test_get_hub_by_id(self, client, test_hub):
        """Test getting hub by ID"""
        response = client.get(f"/hubs/{test_hub.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(test_hub.id)
        assert data["hub_name"] == "Chennai Central Hub"
    
    def test_get_nonexistent_hub(self, client):
        """Test getting non-existent hub"""
        fake_id = str(uuid4())
        response = client.get(f"/hubs/{fake_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_hubs_pagination(self, client, admin_token):
        """Test hub pagination"""
        # Create multiple hubs
        for i in range(5):
            client.post(
                "/hubs",
                headers=auth_header(admin_token),
                json={
                    "hub_name": f"Test Hub {i}",
                    "city": f"City {i}"
                }
            )
        
        response = client.get("/hubs?page=1&page_size=2")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["hubs"]) == 2
        assert data["page"] == 1
        assert data["page_size"] == 2


class TestUpdateHub:
    """Test hub updates"""
    
    def test_admin_update_hub(self, client, admin_token, test_hub):
        """Test admin updating a hub"""
        response = client.put(
            f"/hubs/{test_hub.id}",
            headers=auth_header(admin_token),
            json={
                "capacity": 2000,
                "contact_phone": "+91-44-99999999"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["capacity"] == 2000
        assert data["contact_phone"] == "+91-44-99999999"
    
    def test_agent_cannot_update_hub(self, client, agent_token, test_hub):
        """Test that agent cannot update hub"""
        response = client.put(
            f"/hubs/{test_hub.id}",
            headers=auth_header(agent_token),
            json={"capacity": 2000}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_deactivate_hub(self, client, admin_token, test_hub):
        """Test deactivating a hub"""
        response = client.put(
            f"/hubs/{test_hub.id}",
            headers=auth_header(admin_token),
            json={"is_active": False}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_active"] == False


class TestDeleteHub:
    """Test hub deletion"""
    
    def test_admin_delete_hub(self, client, admin_token, test_hub):
        """Test admin deleting a hub"""
        response = client.delete(
            f"/hubs/{test_hub.id}",
            headers=auth_header(admin_token)
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify deletion
        get_response = client.get(f"/hubs/{test_hub.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_agent_cannot_delete_hub(self, client, agent_token, test_hub):
        """Test that agent cannot delete hub"""
        response = client.delete(
            f"/hubs/{test_hub.id}",
            headers=auth_header(agent_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_customer_cannot_delete_hub(self, client, customer_token, test_hub):
        """Test that customer cannot delete hub"""
        response = client.delete(
            f"/hubs/{test_hub.id}",
            headers=auth_header(customer_token)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
