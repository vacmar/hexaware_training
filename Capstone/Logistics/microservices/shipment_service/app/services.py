"""
Shipment service - Business logic for shipment management
"""
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from .models import Shipment, ShipmentStatus
from .repository import ShipmentRepository
from .schemas import ShipmentCreate, ShipmentUpdate, ShipmentStatusUpdate


class ShipmentNotFoundException(Exception):
    """Exception raised when shipment is not found"""
    def __init__(self, identifier):
        self.identifier = identifier
        self.message = f"Shipment '{identifier}' not found"
        super().__init__(self.message)


class ShipmentCannotBeCancelledException(Exception):
    """Exception raised when shipment cannot be cancelled"""
    def __init__(self, status: str):
        self.status = status
        self.message = f"Shipment with status '{status}' cannot be cancelled"
        super().__init__(self.message)


class UnauthorizedAccessException(Exception):
    """Exception raised for unauthorized access"""
    def __init__(self, message: str = "Unauthorized access"):
        self.message = message
        super().__init__(self.message)


class ShipmentService:
    """Service for shipment operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.shipment_repo = ShipmentRepository(db)
    
    def create_shipment(self, customer_id: UUID, shipment_data: ShipmentCreate) -> Shipment:
        """Create a new shipment"""
        shipment = Shipment(
            customer_id=customer_id,
            source_address=shipment_data.source_address,
            destination_address=shipment_data.destination_address,
            weight=shipment_data.weight,
            dimensions=shipment_data.dimensions,
            description=shipment_data.description,
            current_location=shipment_data.source_address
        )
        
        return self.shipment_repo.create(shipment)
    
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
        customer_id: UUID,
        is_admin: bool = False
    ) -> Shipment:
        """Update a shipment"""
        shipment = self.get_shipment(shipment_id)
        
        # Check authorization
        if not is_admin:
            if shipment.customer_id != customer_id:
                raise UnauthorizedAccessException()
            # Customer can only update if not dispatched
            if shipment.status not in [ShipmentStatus.CREATED]:
                raise UnauthorizedAccessException("Cannot modify shipment after pickup")
        
        return self.shipment_repo.update(shipment, update_data.model_dump(exclude_unset=True))
    
    def update_shipment_status(
        self,
        shipment_id: UUID,
        status_update: ShipmentStatusUpdate
    ) -> Shipment:
        """Update shipment status"""
        shipment = self.get_shipment(shipment_id)
        
        # Update shipment status and location
        update_data = {
            "status": status_update.status,
            "current_location": status_update.location
        }
        return self.shipment_repo.update(shipment, update_data)
    
    def assign_agent(self, shipment_id: UUID, agent_id: UUID) -> Shipment:
        """Assign an agent to a shipment"""
        shipment = self.get_shipment(shipment_id)
        return self.shipment_repo.update(shipment, {"agent_id": agent_id})
    
    def assign_hub(self, shipment_id: UUID, hub_id: UUID) -> Shipment:
        """Assign a hub to a shipment"""
        shipment = self.get_shipment(shipment_id)
        return self.shipment_repo.update(shipment, {"current_hub_id": hub_id})
    
    def cancel_shipment(self, shipment_id: UUID, customer_id: UUID, is_admin: bool = False) -> Shipment:
        """Cancel a shipment"""
        shipment = self.get_shipment(shipment_id)
        
        # Check authorization
        if not is_admin and shipment.customer_id != customer_id:
            raise UnauthorizedAccessException()
        
        # Check if shipment can be cancelled
        if shipment.status not in [ShipmentStatus.CREATED, ShipmentStatus.PICKED_UP]:
            raise ShipmentCannotBeCancelledException(shipment.status.value)
        
        return self.shipment_repo.update(shipment, {"status": ShipmentStatus.CANCELLED})
