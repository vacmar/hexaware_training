"""
Tracking service - Business logic for tracking operations
"""
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
import httpx
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from shared.config import settings
from .models import TrackingUpdate
from .repository import TrackingRepository
from .schemas import TrackingUpdateCreate, ShipmentInfo


class ShipmentNotFoundException(Exception):
    """Exception raised when shipment is not found"""
    def __init__(self, identifier):
        self.identifier = identifier
        self.message = f"Shipment '{identifier}' not found"
        super().__init__(self.message)


class TrackingService:
    """Service for tracking operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.tracking_repo = TrackingRepository(db)
    
    async def get_shipment_info(self, tracking_number: str, token: str = None) -> Optional[ShipmentInfo]:
        """Get shipment info from shipment service"""
        try:
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.SHIPMENT_SERVICE_URL}/shipments/track/{tracking_number}",
                    headers=headers
                )
                if response.status_code == 200:
                    data = response.json()
                    return ShipmentInfo(
                        id=UUID(data["id"]),
                        tracking_number=data["tracking_number"],
                        status=data["status"],
                        current_location=data.get("current_location")
                    )
        except httpx.RequestError:
            pass
        return None
    
    def add_tracking_update(
        self,
        shipment_id: UUID,
        tracking_data: TrackingUpdateCreate
    ) -> TrackingUpdate:
        """Add a tracking update to a shipment"""
        tracking = TrackingUpdate(
            shipment_id=shipment_id,
            location=tracking_data.location,
            status=tracking_data.status,
            description=tracking_data.description
        )
        
        return self.tracking_repo.create(tracking)
    
    def get_tracking_history(self, shipment_id: UUID) -> List[TrackingUpdate]:
        """Get all tracking updates for a shipment"""
        return self.tracking_repo.get_by_shipment(shipment_id)
    
    async def get_tracking_by_tracking_number(self, tracking_number: str, token: str = None) -> Tuple[Optional[ShipmentInfo], List[TrackingUpdate]]:
        """Get tracking history by tracking number"""
        shipment_info = await self.get_shipment_info(tracking_number, token)
        
        if not shipment_info:
            raise ShipmentNotFoundException(tracking_number)
        
        updates = self.tracking_repo.get_by_shipment(shipment_info.id)
        return shipment_info, updates
    
    def get_latest_update(self, shipment_id: UUID) -> Optional[TrackingUpdate]:
        """Get the latest tracking update for a shipment"""
        return self.tracking_repo.get_latest_by_shipment(shipment_id)
