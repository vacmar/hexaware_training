"""
Shipment service - Business logic for shipment management
"""
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from ..models.shipment import Shipment, ShipmentStatus
from ..models.tracking import TrackingUpdate
from ..models.user import User, UserRole
from ..repositories.shipment_repository import ShipmentRepository
from ..repositories.tracking_repository import TrackingRepository
from ..schemas.shipment_schema import ShipmentCreate, ShipmentUpdate, ShipmentStatusUpdate
from ..exceptions.custom_exceptions import (
    ShipmentNotFoundException,
    ShipmentCannotBeCancelledException,
    UnauthorizedAccessException,
    AgentNotFoundException
)


class ShipmentService:
    """Service for shipment operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.shipment_repo = ShipmentRepository(db)
        self.tracking_repo = TrackingRepository(db)
    
    def create_shipment(self, customer_id: UUID, shipment_data: ShipmentCreate) -> Shipment:
        """Create a new shipment"""
        shipment = Shipment(
            customer_id=customer_id,
            source_address=shipment_data.source_address,
            destination_address=shipment_data.destination_address,
            weight=shipment_data.weight,
            dimensions=shipment_data.dimensions,
            description=shipment_data.description
        )
        
        shipment = self.shipment_repo.create(shipment)
        
        # Create initial tracking update
        tracking = TrackingUpdate(
            shipment_id=shipment.id,
            location=shipment_data.source_address,
            status="created",
            description="Shipment created and awaiting pickup"
        )
        self.tracking_repo.create(tracking)
        
        return shipment
    
    def get_shipment(self, shipment_id: UUID) -> Shipment:
        """Get a shipment by ID"""
        shipment = self.shipment_repo.get_by_id(shipment_id)
        if not shipment:
            raise ShipmentNotFoundException(shipment_id)
        return shipment
    
    def get_shipment_by_tracking(self, tracking_number: str) -> Shipment:
        """Get a shipment by tracking number"""
        shipment = self.shipment_repo.get_by_tracking_number(tracking_number)
        if not shipment:
            raise ShipmentNotFoundException(tracking_number)
        return shipment
    
    def get_customer_shipments(
        self,
        customer_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Shipment], int]:
        """Get all shipments for a customer"""
        shipments = self.shipment_repo.get_by_customer(customer_id, skip, limit)
        total = self.shipment_repo.count_by_customer(customer_id)
        return shipments, total
    
    def get_agent_shipments(
        self,
        agent_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Shipment]:
        """Get all shipments assigned to an agent"""
        return self.shipment_repo.get_by_agent(agent_id, skip, limit)
    
    def get_all_shipments(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ShipmentStatus] = None
    ) -> Tuple[List[Shipment], int]:
        """Get all shipments with pagination"""
        shipments = self.shipment_repo.get_all(skip, limit, status)
        total = self.shipment_repo.count(status)
        return shipments, total
    
    def update_shipment(
        self,
        shipment_id: UUID,
        update_data: ShipmentUpdate,
        current_user: User
    ) -> Shipment:
        """Update a shipment (customer can only update their own)"""
        shipment = self.get_shipment(shipment_id)
        
        # Check authorization
        if current_user.role == UserRole.CUSTOMER:
            if shipment.customer_id != current_user.id:
                raise UnauthorizedAccessException()
            # Customer can only update if not dispatched
            if shipment.status not in [ShipmentStatus.CREATED]:
                raise UnauthorizedAccessException("Cannot modify shipment after pickup")
        
        return self.shipment_repo.update(shipment, update_data.model_dump(exclude_unset=True))
    
    def update_shipment_status(
        self,
        shipment_id: UUID,
        status_update: ShipmentStatusUpdate,
        agent: User
    ) -> Shipment:
        """Update shipment status (agent only)"""
        shipment = self.get_shipment(shipment_id)
        
        # Update shipment status and location
        update_data = {
            "status": status_update.status,
            "current_location": status_update.location
        }
        shipment = self.shipment_repo.update(shipment, update_data)
        
        # Create tracking update
        tracking = TrackingUpdate(
            shipment_id=shipment.id,
            location=status_update.location,
            status=status_update.status.value,
            description=status_update.description
        )
        self.tracking_repo.create(tracking)
        
        return shipment
    
    def assign_agent(self, shipment_id: UUID, agent_id: UUID) -> Shipment:
        """Assign an agent to a shipment"""
        shipment = self.get_shipment(shipment_id)
        
        # Verify agent exists
        from ..repositories.user_repository import UserRepository
        user_repo = UserRepository(self.db)
        agent = user_repo.get_by_id(agent_id)
        
        if not agent or agent.role != UserRole.AGENT:
            raise AgentNotFoundException(agent_id)
        
        update_data = {"agent_id": agent_id}
        return self.shipment_repo.update(shipment, update_data)
    
    def cancel_shipment(self, shipment_id: UUID, current_user: User) -> Shipment:
        """Cancel a shipment"""
        shipment = self.get_shipment(shipment_id)
        
        # Check authorization
        if current_user.role == UserRole.CUSTOMER:
            if shipment.customer_id != current_user.id:
                raise UnauthorizedAccessException()
        
        # Check if can be cancelled
        if not self.shipment_repo.can_cancel(shipment):
            raise ShipmentCannotBeCancelledException(shipment.tracking_number)
        
        update_data = {"status": ShipmentStatus.CANCELLED}
        shipment = self.shipment_repo.update(shipment, update_data)
        
        # Add tracking update
        tracking = TrackingUpdate(
            shipment_id=shipment.id,
            location=shipment.current_location or shipment.source_address,
            status="cancelled",
            description="Shipment cancelled by customer"
        )
        self.tracking_repo.create(tracking)
        
        return shipment
    
    def delete_shipment(self, shipment_id: UUID, current_user: User) -> bool:
        """Delete a shipment"""
        shipment = self.get_shipment(shipment_id)
        
        # Check authorization
        if current_user.role == UserRole.CUSTOMER:
            if shipment.customer_id != current_user.id:
                raise UnauthorizedAccessException()
            # Customer can only delete if not dispatched
            if shipment.status not in [ShipmentStatus.CREATED, ShipmentStatus.CANCELLED]:
                raise UnauthorizedAccessException("Cannot delete shipment after pickup")
        
        return self.shipment_repo.delete(shipment)
    
    def get_shipment_stats(self) -> dict:
        """Get shipment statistics for today"""
        status_counts = self.shipment_repo.count_by_status_today()
        total_today = self.shipment_repo.count_today()
        
        return {
            "total_shipments_today": total_today,
            "delivered": status_counts.get("delivered", 0),
            "in_transit": status_counts.get("in_transit", 0),
            "out_for_delivery": status_counts.get("out_for_delivery", 0),
            "created": status_counts.get("created", 0),
            "cancelled": status_counts.get("cancelled", 0)
        }
