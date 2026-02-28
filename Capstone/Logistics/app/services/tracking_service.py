"""
Tracking service - Business logic for tracking operations
"""
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from ..models.tracking import TrackingUpdate
from ..repositories.tracking_repository import TrackingRepository
from ..repositories.shipment_repository import ShipmentRepository
from ..schemas.tracking_schema import TrackingUpdateCreate
from ..exceptions.custom_exceptions import ShipmentNotFoundException


class TrackingService:
    """Service for tracking operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.tracking_repo = TrackingRepository(db)
        self.shipment_repo = ShipmentRepository(db)
    
    def add_tracking_update(
        self,
        shipment_id: UUID,
        tracking_data: TrackingUpdateCreate
    ) -> TrackingUpdate:
        """Add a tracking update to a shipment"""
        # Verify shipment exists
        shipment = self.shipment_repo.get_by_id(shipment_id)
        if not shipment:
            raise ShipmentNotFoundException(shipment_id)
        
        tracking = TrackingUpdate(
            shipment_id=shipment_id,
            location=tracking_data.location,
            status=tracking_data.status,
            description=tracking_data.description
        )
        
        # Update shipment's current location
        self.shipment_repo.update(shipment, {"current_location": tracking_data.location})
        
        return self.tracking_repo.create(tracking)
    
    def get_tracking_history(self, shipment_id: UUID) -> List[TrackingUpdate]:
        """Get all tracking updates for a shipment"""
        # Verify shipment exists
        shipment = self.shipment_repo.get_by_id(shipment_id)
        if not shipment:
            raise ShipmentNotFoundException(shipment_id)
        
        return self.tracking_repo.get_by_shipment(shipment_id)
    
    def get_tracking_by_tracking_number(self, tracking_number: str) -> tuple:
        """Get tracking history by tracking number"""
        shipment = self.shipment_repo.get_by_tracking_number(tracking_number)
        if not shipment:
            raise ShipmentNotFoundException(tracking_number)
        
        updates = self.tracking_repo.get_by_shipment(shipment.id)
        return shipment, updates
    
    def get_latest_update(self, shipment_id: UUID) -> TrackingUpdate:
        """Get the latest tracking update for a shipment"""
        return self.tracking_repo.get_latest_by_shipment(shipment_id)
