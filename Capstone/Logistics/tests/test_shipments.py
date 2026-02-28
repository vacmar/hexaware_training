"""
Shipment tests
"""
import pytest
from uuid import uuid4
from fastapi import status

from tests.conftest import auth_header


class TestCreateShipment:
    """Test shipment creation"""
    
    def test_create_shipment_success(self, client, customer_token):
        """Test successful shipment creation"""
        response = client.post(
            "/shipments",
            headers=auth_header(customer_token),
            json={
                "source_address": "Chennai, Tamil Nadu",
                "destination_address": "Bangalore, Karnataka",
                "weight": 2.5,
                "dimensions": "10x20x30",
                "description": "Electronics package"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "tracking_number" in data
        assert data["tracking_number"].startswith("TRK")
        assert data["status"] == "created"
        assert data["source_address"] == "Chennai, Tamil Nadu"
        assert data["destination_address"] == "Bangalore, Karnataka"
    
    def test_create_shipment_minimal(self, client, customer_token):
        """Test shipment creation with minimal data"""
        response = client.post(
            "/shipments",
            headers=auth_header(customer_token),
            json={
                "source_address": "Chennai",
                "destination_address": "Bangalore"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["weight"] is None
        assert data["dimensions"] is None
    
    def test_create_shipment_unauthenticated(self, client):
        """Test shipment creation without authentication"""
        response = client.post(
            "/shipments",
            json={
                "source_address": "Chennai",
                "destination_address": "Bangalore"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_shipment_missing_fields(self, client, customer_token):
        """Test shipment creation with missing required fields"""
        response = client.post(
            "/shipments",
            headers=auth_header(customer_token),
            json={
                "source_address": "Chennai"
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetShipments:
    """Test getting shipments"""
    
    def test_get_customer_shipments(self, client, customer_token):
        """Test getting customer's shipments"""
        # Create a shipment first
        client.post(
            "/shipments",
            headers=auth_header(customer_token),
            json={
                "source_address": "Chennai",
                "destination_address": "Bangalore"
            }
        )
        
        response = client.get(
            "/shipments",
            headers=auth_header(customer_token)
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "shipments" in data
        assert "total" in data
        assert len(data["shipments"]) >= 1
    
    def test_get_shipments_pagination(self, client, customer_token):
        """Test shipment pagination"""
        # Create multiple shipments
        for i in range(5):
            client.post(
                "/shipments",
                headers=auth_header(customer_token),
                json={
                    "source_address": f"City {i}",
                    "destination_address": f"City {i+1}"
                }
            )
        
        response = client.get(
            "/shipments?page=1&page_size=2",
            headers=auth_header(customer_token)
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["shipments"]) == 2
        assert data["page"] == 1
        assert data["page_size"] == 2


class TestTrackShipment:
    """Test shipment tracking"""
    
    def test_track_shipment_by_tracking_number(self, client, customer_token):
        """Test tracking a shipment by tracking number"""
        # Create a shipment
        create_response = client.post(
            "/shipments",
            headers=auth_header(customer_token),
            json={
                "source_address": "Chennai",
                "destination_address": "Bangalore"
            }
        )
        tracking_number = create_response.json()["tracking_number"]
        
        # Track the shipment (public endpoint)
        response = client.get(f"/shipments/track/{tracking_number}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["tracking_number"] == tracking_number
        assert data["status"] == "created"
    
    def test_track_nonexistent_shipment(self, client):
        """Test tracking non-existent shipment"""
        response = client.get("/shipments/track/TRKNONEXISTENT")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateShipmentStatus:
    """Test shipment status updates"""
    
    def test_agent_update_status(self, client, customer_token, agent_token):
        """Test agent updating shipment status"""
        # Create a shipment
        create_response = client.post(
            "/shipments",
            headers=auth_header(customer_token),
            json={
                "source_address": "Chennai",
                "destination_address": "Bangalore"
            }
        )
        shipment_id = create_response.json()["id"]
        
        # Agent updates status
        response = client.put(
            f"/shipments/{shipment_id}/status",
            headers=auth_header(agent_token),
            json={
                "status": "in_transit",
                "location": "Salem Hub",
                "description": "Package arrived at Salem hub"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "in_transit"
        assert data["current_location"] == "Salem Hub"
    
    def test_customer_cannot_update_status(self, client, customer_token):
        """Test that customer cannot update shipment status"""
        # Create a shipment
        create_response = client.post(
            "/shipments",
            headers=auth_header(customer_token),
            json={
                "source_address": "Chennai",
                "destination_address": "Bangalore"
            }
        )
        shipment_id = create_response.json()["id"]
        
        # Customer tries to update status
        response = client.put(
            f"/shipments/{shipment_id}/status",
            headers=auth_header(customer_token),
            json={
                "status": "in_transit",
                "location": "Salem Hub"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestCancelShipment:
    """Test shipment cancellation"""
    
    def test_cancel_shipment_success(self, client, customer_token):
        """Test successful shipment cancellation"""
        # Create a shipment
        create_response = client.post(
            "/shipments",
            headers=auth_header(customer_token),
            json={
                "source_address": "Chennai",
                "destination_address": "Bangalore"
            }
        )
        shipment_id = create_response.json()["id"]
        
        # Cancel the shipment
        response = client.delete(
            f"/shipments/{shipment_id}",
            headers=auth_header(customer_token)
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_cancel_dispatched_shipment(self, client, customer_token, agent_token):
        """Test cancelling a dispatched shipment (should fail)"""
        # Create a shipment
        create_response = client.post(
            "/shipments",
            headers=auth_header(customer_token),
            json={
                "source_address": "Chennai",
                "destination_address": "Bangalore"
            }
        )
        shipment_id = create_response.json()["id"]
        
        # Agent dispatches the shipment
        client.put(
            f"/shipments/{shipment_id}/status",
            headers=auth_header(agent_token),
            json={
                "status": "in_transit",
                "location": "Salem Hub"
            }
        )
        
        # Try to cancel
        response = client.delete(
            f"/shipments/{shipment_id}",
            headers=auth_header(customer_token)
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestAssignAgent:
    """Test agent assignment"""
    
    def test_admin_assign_agent(self, client, customer_token, admin_token, test_agent):
        """Test admin assigning agent to shipment"""
        # Create a shipment
        create_response = client.post(
            "/shipments",
            headers=auth_header(customer_token),
            json={
                "source_address": "Chennai",
                "destination_address": "Bangalore"
            }
        )
        shipment_id = create_response.json()["id"]
        
        # Admin assigns agent
        response = client.put(
            f"/shipments/{shipment_id}/assign-agent",
            headers=auth_header(admin_token),
            json={"agent_id": str(test_agent.id)}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["agent_id"] == str(test_agent.id)
    
    def test_customer_cannot_assign_agent(self, client, customer_token, test_agent):
        """Test that customer cannot assign agent"""
        # Create a shipment
        create_response = client.post(
            "/shipments",
            headers=auth_header(customer_token),
            json={
                "source_address": "Chennai",
                "destination_address": "Bangalore"
            }
        )
        shipment_id = create_response.json()["id"]
        
        # Customer tries to assign agent
        response = client.put(
            f"/shipments/{shipment_id}/assign-agent",
            headers=auth_header(customer_token),
            json={"agent_id": str(test_agent.id)}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
