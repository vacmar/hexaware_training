"""
Tracking repository - Data access layer for tracking updates
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from ..models.tracking import TrackingUpdate


class TrackingRepository:
    """Repository for TrackingUpdate model operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, tracking_update: TrackingUpdate) -> TrackingUpdate:
        """Create a new tracking update"""
        self.db.add(tracking_update)
        self.db.commit()
        self.db.refresh(tracking_update)
        return tracking_update
    
    def get_by_id(self, tracking_id: UUID) -> Optional[TrackingUpdate]:
        """Get tracking update by ID"""
        return self.db.query(TrackingUpdate).filter(TrackingUpdate.id == tracking_id).first()
    
    def get_by_shipment(self, shipment_id: UUID) -> List[TrackingUpdate]:
        """Get all tracking updates for a shipment"""
        return self.db.query(TrackingUpdate).filter(
            TrackingUpdate.shipment_id == shipment_id
        ).order_by(TrackingUpdate.created_at.desc()).all()
    
    def get_latest_by_shipment(self, shipment_id: UUID) -> Optional[TrackingUpdate]:
        """Get the latest tracking update for a shipment"""
        return self.db.query(TrackingUpdate).filter(
            TrackingUpdate.shipment_id == shipment_id
        ).order_by(TrackingUpdate.created_at.desc()).first()
    
    def count_by_shipment(self, shipment_id: UUID) -> int:
        """Count tracking updates for a shipment"""
        return self.db.query(TrackingUpdate).filter(
            TrackingUpdate.shipment_id == shipment_id
        ).count()
    
    def delete_by_shipment(self, shipment_id: UUID) -> int:
        """Delete all tracking updates for a shipment"""
        count = self.db.query(TrackingUpdate).filter(
            TrackingUpdate.shipment_id == shipment_id
        ).delete()
        self.db.commit()
        return count
