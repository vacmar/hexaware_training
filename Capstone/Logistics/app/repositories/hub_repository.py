"""
Hub repository - Data access layer for hubs
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from ..models.hub import Hub


class HubRepository:
    """Repository for Hub model operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, hub: Hub) -> Hub:
        """Create a new hub"""
        self.db.add(hub)
        self.db.commit()
        self.db.refresh(hub)
        return hub
    
    def get_by_id(self, hub_id: UUID) -> Optional[Hub]:
        """Get hub by ID"""
        return self.db.query(Hub).filter(Hub.id == hub_id).first()
    
    def get_by_name(self, hub_name: str) -> Optional[Hub]:
        """Get hub by name"""
        return self.db.query(Hub).filter(Hub.hub_name == hub_name).first()
    
    def get_by_city(self, city: str) -> List[Hub]:
        """Get all hubs in a city"""
        return self.db.query(Hub).filter(Hub.city == city).all()
    
    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = False) -> List[Hub]:
        """Get all hubs with optional filtering"""
        query = self.db.query(Hub)
        if active_only:
            query = query.filter(Hub.is_active == True)
        return query.order_by(Hub.hub_name).offset(skip).limit(limit).all()
    
    def count(self, active_only: bool = False) -> int:
        """Count hubs"""
        query = self.db.query(Hub)
        if active_only:
            query = query.filter(Hub.is_active == True)
        return query.count()
    
    def update(self, hub: Hub, update_data: dict) -> Hub:
        """Update hub fields"""
        for key, value in update_data.items():
            if value is not None:
                setattr(hub, key, value)
        self.db.commit()
        self.db.refresh(hub)
        return hub
    
    def delete(self, hub: Hub) -> bool:
        """Delete a hub"""
        self.db.delete(hub)
        self.db.commit()
        return True
