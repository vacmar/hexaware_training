"""
Hub service - Business logic for hub management
"""
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from ..models.hub import Hub
from ..repositories.hub_repository import HubRepository
from ..schemas.hub_schema import HubCreate, HubUpdate
from ..exceptions.custom_exceptions import HubNotFoundException, HubAlreadyExistsException


class HubService:
    """Service for hub management operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.hub_repo = HubRepository(db)
    
    def create_hub(self, hub_data: HubCreate) -> Hub:
        """Create a new hub"""
        # Check if hub with same name exists
        existing_hub = self.hub_repo.get_by_name(hub_data.hub_name)
        if existing_hub:
            raise HubAlreadyExistsException(hub_data.hub_name)
        
        hub = Hub(
            hub_name=hub_data.hub_name,
            city=hub_data.city,
            address=hub_data.address,
            contact_phone=hub_data.contact_phone,
            contact_email=hub_data.contact_email,
            capacity=hub_data.capacity
        )
        
        return self.hub_repo.create(hub)
    
    def get_hub(self, hub_id: UUID) -> Hub:
        """Get a hub by ID"""
        hub = self.hub_repo.get_by_id(hub_id)
        if not hub:
            raise HubNotFoundException(hub_id)
        return hub
    
    def get_all_hubs(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False
    ) -> Tuple[List[Hub], int]:
        """Get all hubs with pagination"""
        hubs = self.hub_repo.get_all(skip, limit, active_only)
        total = self.hub_repo.count(active_only)
        return hubs, total
    
    def get_hubs_by_city(self, city: str) -> List[Hub]:
        """Get all hubs in a city"""
        return self.hub_repo.get_by_city(city)
    
    def update_hub(self, hub_id: UUID, update_data: HubUpdate) -> Hub:
        """Update a hub"""
        hub = self.get_hub(hub_id)
        
        # Check if new name conflicts with existing hub
        if update_data.hub_name:
            existing_hub = self.hub_repo.get_by_name(update_data.hub_name)
            if existing_hub and existing_hub.id != hub_id:
                raise HubAlreadyExistsException(update_data.hub_name)
        
        return self.hub_repo.update(hub, update_data.model_dump(exclude_unset=True))
    
    def delete_hub(self, hub_id: UUID) -> bool:
        """Delete a hub"""
        hub = self.get_hub(hub_id)
        return self.hub_repo.delete(hub)
    
    def get_hub_count(self) -> int:
        """Get total hub count"""
        return self.hub_repo.count()
