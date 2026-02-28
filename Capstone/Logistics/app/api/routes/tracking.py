"""
Tracking routes
"""
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.dependencies import require_agent
from ...models.user import User
from ...services.tracking_service import TrackingService
from ...schemas.tracking_schema import (
    TrackingUpdateCreate,
    TrackingUpdateResponse,
    TrackingHistoryResponse
)

router = APIRouter()


@router.post("/{shipment_id}", response_model=TrackingUpdateResponse, status_code=status.HTTP_201_CREATED)
def add_tracking_update(
    shipment_id: UUID,
    tracking_data: TrackingUpdateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_agent)
):
    """
    Add a tracking update to a shipment.
    
    Accessible by delivery agents and admins only.
    """
    service = TrackingService(db)
    tracking = service.add_tracking_update(shipment_id, tracking_data)
    return tracking


@router.get("/{shipment_id}", response_model=TrackingHistoryResponse)
def get_tracking_history(
    shipment_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get tracking history for a shipment.
    
    Public endpoint - no authentication required.
    """
    service = TrackingService(db)
    updates = service.get_tracking_history(shipment_id)
    
    # Get shipment for tracking number
    from ...repositories.shipment_repository import ShipmentRepository
    shipment_repo = ShipmentRepository(db)
    shipment = shipment_repo.get_by_id(shipment_id)
    
    return TrackingHistoryResponse(
        tracking_number=shipment.tracking_number if shipment else str(shipment_id),
        updates=updates,
        total_updates=len(updates)
    )


@router.get("/number/{tracking_number}", response_model=TrackingHistoryResponse)
def get_tracking_by_number(
    tracking_number: str,
    db: Session = Depends(get_db)
):
    """
    Get tracking history by tracking number.
    
    Public endpoint - no authentication required.
    """
    service = TrackingService(db)
    shipment, updates = service.get_tracking_by_tracking_number(tracking_number)
    
    return TrackingHistoryResponse(
        tracking_number=tracking_number,
        updates=updates,
        total_updates=len(updates)
    )
