"""
Tracking Service Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from shared.database import get_db
from shared.security import decode_access_token
from .services import TrackingService, ShipmentNotFoundException
from .schemas import TrackingUpdateCreate, TrackingUpdateResponse, TrackingHistoryResponse

tracking_router = APIRouter()


async def get_current_user_optional(authorization: str = Header(None)):
    """Get current user from token (optional)"""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    return payload


async def get_current_user(authorization: str = Header(...)):
    """Get current user from token (required)"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    return payload


async def require_agent_or_admin(user: dict = Depends(get_current_user)):
    """Require agent or admin role"""
    if user.get("role") not in ["agent", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Agent or admin access required"
        )
    return user


@tracking_router.post("/{shipment_id}", response_model=TrackingUpdateResponse, status_code=status.HTTP_201_CREATED)
async def add_tracking_update(
    shipment_id: UUID,
    tracking_data: TrackingUpdateCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_agent_or_admin)
):
    """Add a tracking update to a shipment (agent/admin only)"""
    tracking_service = TrackingService(db)
    tracking = tracking_service.add_tracking_update(shipment_id, tracking_data)
    return tracking


@tracking_router.get("/{shipment_id}", response_model=List[TrackingUpdateResponse])
def get_tracking_history(
    shipment_id: UUID,
    db: Session = Depends(get_db)
):
    """Get tracking history for a shipment by ID"""
    tracking_service = TrackingService(db)
    return tracking_service.get_tracking_history(shipment_id)


@tracking_router.get("/track/{tracking_number}", response_model=TrackingHistoryResponse)
async def get_tracking_by_number(
    tracking_number: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Get tracking history by tracking number (public)"""
    try:
        token = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
        
        tracking_service = TrackingService(db)
        shipment_info, updates = await tracking_service.get_tracking_by_tracking_number(tracking_number, token)
        
        return TrackingHistoryResponse(
            shipment_id=shipment_info.id,
            tracking_number=shipment_info.tracking_number,
            current_status=shipment_info.status,
            current_location=shipment_info.current_location,
            updates=updates
        )
    except ShipmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@tracking_router.get("/{shipment_id}/latest", response_model=TrackingUpdateResponse)
def get_latest_tracking(
    shipment_id: UUID,
    db: Session = Depends(get_db)
):
    """Get the latest tracking update for a shipment"""
    tracking_service = TrackingService(db)
    latest = tracking_service.get_latest_update(shipment_id)
    if not latest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tracking updates found for this shipment"
        )
    return latest
