"""
Shipment repository - Data access layer for shipments
"""
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from ..models.shipment import Shipment, ShipmentStatus


class ShipmentRepository:
    """Repository for Shipment model operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, shipment: Shipment) -> Shipment:
        """Create a new shipment"""
        self.db.add(shipment)
        self.db.commit()
        self.db.refresh(shipment)
        return shipment
    
    def get_by_id(self, shipment_id: UUID) -> Optional[Shipment]:
        """Get shipment by ID"""
        return self.db.query(Shipment).filter(Shipment.id == shipment_id).first()
    
    def get_by_tracking_number(self, tracking_number: str) -> Optional[Shipment]:
        """Get shipment by tracking number"""
        return self.db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    
    def get_by_customer(self, customer_id: UUID, skip: int = 0, limit: int = 100) -> List[Shipment]:
        """Get all shipments for a customer"""
        return self.db.query(Shipment).filter(
            Shipment.customer_id == customer_id
        ).order_by(Shipment.created_at.desc()).offset(skip).limit(limit).all()
    
    def count_by_customer(self, customer_id: UUID) -> int:
        """Count shipments for a customer"""
        return self.db.query(Shipment).filter(Shipment.customer_id == customer_id).count()
    
    def get_by_agent(self, agent_id: UUID, skip: int = 0, limit: int = 100) -> List[Shipment]:
        """Get all shipments assigned to an agent"""
        return self.db.query(Shipment).filter(
            Shipment.agent_id == agent_id
        ).order_by(Shipment.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_all(self, skip: int = 0, limit: int = 100, status: Optional[ShipmentStatus] = None) -> List[Shipment]:
        """Get all shipments with optional filtering"""
        query = self.db.query(Shipment)
        if status:
            query = query.filter(Shipment.status == status)
        return query.order_by(Shipment.created_at.desc()).offset(skip).limit(limit).all()
    
    def count(self, status: Optional[ShipmentStatus] = None) -> int:
        """Count shipments with optional status filter"""
        query = self.db.query(Shipment)
        if status:
            query = query.filter(Shipment.status == status)
        return query.count()
    
    def count_today(self, status: Optional[ShipmentStatus] = None) -> int:
        """Count today's shipments"""
        today = date.today()
        query = self.db.query(Shipment).filter(
            func.date(Shipment.created_at) == today
        )
        if status:
            query = query.filter(Shipment.status == status)
        return query.count()
    
    def count_by_status_today(self) -> dict:
        """Get count of shipments by status for today"""
        today = date.today()
        result = self.db.query(
            Shipment.status, func.count(Shipment.id)
        ).filter(
            func.date(Shipment.created_at) == today
        ).group_by(Shipment.status).all()
        return {status.value: count for status, count in result}
    
    def update(self, shipment: Shipment, update_data: dict) -> Shipment:
        """Update shipment fields"""
        for key, value in update_data.items():
            if value is not None:
                setattr(shipment, key, value)
        self.db.commit()
        self.db.refresh(shipment)
        return shipment
    
    def delete(self, shipment: Shipment) -> bool:
        """Delete a shipment"""
        self.db.delete(shipment)
        self.db.commit()
        return True
    
    def can_cancel(self, shipment: Shipment) -> bool:
        """Check if shipment can be cancelled"""
        return shipment.status in [ShipmentStatus.CREATED, ShipmentStatus.PICKED_UP]
