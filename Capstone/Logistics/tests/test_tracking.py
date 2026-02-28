"""
Tracking tests
"""
import pytest
from fastapi import status

from tests.conftest import auth_header


class TestAddTrackingUpdate:
    """Test adding tracking updates"""
    
    def test_agent_add_tracking_update(self, client, customer_token, agent_token):
        """Test agent adding tracking update"""
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
        
        # Agent adds tracking update
        response = client.post(
            f"/tracking/{shipment_id}",
            headers=auth_header(agent_token),
            json={
                "location": "Salem Hub",
                "status": "in_transit",
                "description": "Package scanned at Salem hub"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["location"] == "Salem Hub"
        assert data["status"] == "in_transit"
    
    def test_customer_cannot_add_tracking(self, client, customer_token):
        """Test that customer cannot add tracking update"""
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
        
        # Customer tries to add tracking
        response = client.post(
            f"/tracking/{shipment_id}",
            headers=auth_header(customer_token),
            json={
                "location": "My House",
                "status": "delivered"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestGetTrackingHistory:
    """Test getting tracking history"""
    
    def test_get_tracking_history(self, client, customer_token, agent_token):
        """Test getting tracking history for a shipment"""
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
        
        # Add multiple tracking updates
        locations = [
            ("Chennai Pickup Point", "picked_up"),
            ("Salem Hub", "in_transit"),
            ("Bangalore Hub", "at_hub"),
        ]
        
        for location, status_val in locations:
            client.post(
                f"/tracking/{shipment_id}",
                headers=auth_header(agent_token),
                json={
                    "location": location,
                    "status": status_val
                }
            )
        
        # Get tracking history
        response = client.get(f"/tracking/{shipment_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "updates" in data
        # Initial "created" + 3 added = 4 total (but created is auto-added in service)
        assert len(data["updates"]) >= 3
    
    def test_get_tracking_by_tracking_number(self, client, customer_token, agent_token):
        """Test getting tracking by tracking number"""
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
        shipment_id = create_response.json()["id"]
        
        # Add a tracking update
        client.post(
            f"/tracking/{shipment_id}",
            headers=auth_header(agent_token),
            json={
                "location": "Salem Hub",
                "status": "in_transit"
            }
        )
        
        # Get tracking by number
        response = client.get(f"/tracking/number/{tracking_number}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["tracking_number"] == tracking_number
        assert len(data["updates"]) >= 1
    
    def test_get_tracking_nonexistent(self, client):
        """Test getting tracking for non-existent shipment"""
        from uuid import uuid4
        fake_id = str(uuid4())
        response = client.get(f"/tracking/{fake_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestTrackingFlow:
    """Test complete tracking flow"""
    
    def test_complete_delivery_flow(self, client, customer_token, agent_token):
        """Test complete delivery tracking flow"""
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
        tracking_number = create_response.json()["tracking_number"]
        
        # Simulate delivery flow
        flow_steps = [
            ("picked_up", "Chennai Pickup Point", "Package picked up from sender"),
            ("in_transit", "Chennai Main Hub", "Package at Chennai hub"),
            ("in_transit", "Salem Transit Hub", "Package in transit"),
            ("at_hub", "Bangalore Main Hub", "Package arrived at Bangalore"),
            ("out_for_delivery", "Bangalore Delivery Center", "Out for delivery"),
            ("delivered", "Customer Address", "Package delivered to customer"),
        ]
        
        for status_val, location, description in flow_steps:
            # Update status
            client.put(
                f"/shipments/{shipment_id}/status",
                headers=auth_header(agent_token),
                json={
                    "status": status_val,
                    "location": location,
                    "description": description
                }
            )
        
        # Verify final state
        track_response = client.get(f"/shipments/track/{tracking_number}")
        assert track_response.status_code == status.HTTP_200_OK
        data = track_response.json()
        assert data["status"] == "delivered"
        assert data["current_location"] == "Customer Address"
        
        # Verify tracking history
        history_response = client.get(f"/tracking/{shipment_id}")
        history_data = history_response.json()
        # Initial created + 6 updates
        assert len(history_data["updates"]) >= 6
