"""
Shipment routes
"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.dependencies import (
    get_current_user,
    require_agent,
    require_admin,
    require_any_authenticated
)
from ...models.user import User, UserRole
from ...models.shipment import ShipmentStatus
from ...services.shipment_service import ShipmentService
from ...schemas.shipment_schema import (
    ShipmentCreate,
    ShipmentUpdate,
    ShipmentStatusUpdate,
    ShipmentResponse,
    ShipmentDetailResponse,
    ShipmentTrackResponse,
    ShipmentListResponse,
    ShipmentAssignAgent
)

router = APIRouter()


@router.post("", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
def create_shipment(
    shipment_data: ShipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new shipment.
    
    Accessible by authenticated customers.
    """
    service = ShipmentService(db)
    shipment = service.create_shipment(current_user.id, shipment_data)
    return shipment


@router.get("", response_model=ShipmentListResponse)
def get_shipments(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[ShipmentStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all shipments for the current user.
    
    - Customers see their own shipments
    - Agents see their assigned shipments
    - Admins see all shipments
    """
    service = ShipmentService(db)
    skip = (page - 1) * page_size
    
    if current_user.role == UserRole.CUSTOMER:
        shipments, total = service.get_customer_shipments(current_user.id, skip, page_size)
    elif current_user.role == UserRole.AGENT:
        shipments = service.get_agent_shipments(current_user.id, skip, page_size)
        total = len(shipments)
    else:
        shipments, total = service.get_all_shipments(skip, page_size, status)
    
    return ShipmentListResponse(
        shipments=shipments,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/track/{tracking_number}", response_model=ShipmentTrackResponse)
def track_shipment(tracking_number: str, db: Session = Depends(get_db)):
    """
    Track a shipment by tracking number.
    
    Public endpoint - no authentication required.
    """
    service = ShipmentService(db)
    shipment = service.get_shipment_by_tracking(tracking_number)
    return ShipmentTrackResponse(
        tracking_number=shipment.tracking_number,
        status=shipment.status,
        current_location=shipment.current_location,
        source_address=shipment.source_address,
        destination_address=shipment.destination_address,
        tracking_updates=shipment.tracking_updates
    )


@router.get("/{shipment_id}", response_model=ShipmentDetailResponse)
def get_shipment(
    shipment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get shipment details by ID.
    """
    service = ShipmentService(db)
    shipment = service.get_shipment(shipment_id)
    return shipment


@router.put("/{shipment_id}", response_model=ShipmentResponse)
def update_shipment(
    shipment_id: UUID,
    update_data: ShipmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a shipment.
    
    Customers can only update their own shipments before dispatch.
    """
    service = ShipmentService(db)
    shipment = service.update_shipment(shipment_id, update_data, current_user)
    return shipment


@router.put("/{shipment_id}/status", response_model=ShipmentResponse)
def update_shipment_status(
    shipment_id: UUID,
    status_update: ShipmentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_agent)
):
    """
    Update shipment status.
    
    Accessible by delivery agents and admins only.
    """
    service = ShipmentService(db)
    shipment = service.update_shipment_status(shipment_id, status_update, current_user)
    return shipment


@router.put("/{shipment_id}/assign-agent", response_model=ShipmentResponse)
def assign_agent(
    shipment_id: UUID,
    assign_data: ShipmentAssignAgent,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Assign an agent to a shipment.
    
    Admin only.
    """
    service = ShipmentService(db)
    shipment = service.assign_agent(shipment_id, assign_data.agent_id)
    return shipment


@router.delete("/{shipment_id}", status_code=status.HTTP_200_OK)
def cancel_shipment(
    shipment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cancel a shipment.
    
    Can only cancel shipments that haven't been dispatched yet.
    """
    service = ShipmentService(db)
    service.cancel_shipment(shipment_id, current_user)
    return {"message": "Shipment cancelled successfully"}
