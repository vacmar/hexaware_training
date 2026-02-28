"""
Shipment Service Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
import sys
import os
import httpx
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from shared.database import get_db
from shared.config import settings
from shared.security import decode_access_token
from .services import (
    ShipmentService, 
    ShipmentNotFoundException, 
    ShipmentCannotBeCancelledException,
    UnauthorizedAccessException
)
from .schemas import (
    ShipmentCreate, 
    ShipmentUpdate, 
    ShipmentStatusUpdate,
    ShipmentResponse, 
    ShipmentListResponse,
    AssignAgentRequest,
    ShipmentStatus
)

shipment_router = APIRouter()


async def get_current_user(authorization: str = Header(None)):
    """Get current user from token"""
    if not authorization or not authorization.startswith("Bearer "):
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


async def require_admin(user: dict = Depends(get_current_user)):
    """Require admin role"""
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user


@shipment_router.post("/", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment(
    shipment_data: ShipmentCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Create a new shipment"""
    shipment_service = ShipmentService(db)
    customer_id = UUID(user.get("sub"))
    shipment = shipment_service.create_shipment(customer_id, shipment_data)
    return shipment


@shipment_router.get("/", response_model=ShipmentListResponse)
async def get_all_shipments(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ShipmentStatus] = None,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    """Get all shipments (admin only)"""
    shipment_service = ShipmentService(db)
    shipments, total = shipment_service.get_all_shipments(skip, limit, status)
    return ShipmentListResponse(shipments=shipments, total=total, skip=skip, limit=limit)


@shipment_router.get("/my", response_model=ShipmentListResponse)
async def get_my_shipments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Get current user's shipments"""
    shipment_service = ShipmentService(db)
    customer_id = UUID(user.get("sub"))
    shipments, total = shipment_service.get_customer_shipments(customer_id, skip, limit)
    return ShipmentListResponse(shipments=shipments, total=total, skip=skip, limit=limit)


@shipment_router.get("/agent/assigned", response_model=ShipmentListResponse)
async def get_assigned_shipments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: dict = Depends(require_agent_or_admin)
):
    """Get shipments assigned to current agent"""
    shipment_service = ShipmentService(db)
    agent_id = UUID(user.get("sub"))
    shipments = shipment_service.get_agent_shipments(agent_id, skip, limit)
    return ShipmentListResponse(shipments=shipments, total=len(shipments), skip=skip, limit=limit)


@shipment_router.get("/track/{tracking_number}", response_model=ShipmentResponse)
def get_shipment_by_tracking(
    tracking_number: str,
    db: Session = Depends(get_db)
):
    """Get shipment by tracking number (public)"""
    try:
        shipment_service = ShipmentService(db)
        return shipment_service.get_shipment_by_tracking(tracking_number)
    except ShipmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@shipment_router.get("/{shipment_id}", response_model=ShipmentResponse)
async def get_shipment(
    shipment_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Get a specific shipment"""
    try:
        shipment_service = ShipmentService(db)
        shipment = shipment_service.get_shipment(shipment_id)
        
        # Check authorization
        user_id = UUID(user.get("sub"))
        user_role = user.get("role")
        
        if user_role == "customer" and shipment.customer_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this shipment"
            )
        
        return shipment
    except ShipmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@shipment_router.put("/{shipment_id}", response_model=ShipmentResponse)
async def update_shipment(
    shipment_id: UUID,
    update_data: ShipmentUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Update a shipment"""
    try:
        shipment_service = ShipmentService(db)
        customer_id = UUID(user.get("sub"))
        is_admin = user.get("role") == "admin"
        return shipment_service.update_shipment(shipment_id, update_data, customer_id, is_admin)
    except ShipmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UnauthorizedAccessException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@shipment_router.patch("/{shipment_id}/status", response_model=ShipmentResponse)
async def update_shipment_status(
    shipment_id: UUID,
    status_update: ShipmentStatusUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_agent_or_admin)
):
    """Update shipment status (agent/admin only)"""
    try:
        shipment_service = ShipmentService(db)
        return shipment_service.update_shipment_status(shipment_id, status_update)
    except ShipmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@shipment_router.patch("/{shipment_id}/assign-agent", response_model=ShipmentResponse)
async def assign_agent(
    shipment_id: UUID,
    request: AssignAgentRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    """Assign an agent to a shipment (admin only)"""
    try:
        shipment_service = ShipmentService(db)
        return shipment_service.assign_agent(shipment_id, request.agent_id)
    except ShipmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@shipment_router.patch("/{shipment_id}/assign-hub")
async def assign_hub(
    shipment_id: UUID,
    hub_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    """Assign a hub to a shipment (admin only)"""
    try:
        shipment_service = ShipmentService(db)
        return shipment_service.assign_hub(shipment_id, hub_id)
    except ShipmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@shipment_router.post("/{shipment_id}/cancel", response_model=ShipmentResponse)
async def cancel_shipment(
    shipment_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Cancel a shipment"""
    try:
        shipment_service = ShipmentService(db)
        customer_id = UUID(user.get("sub"))
        is_admin = user.get("role") == "admin"
        return shipment_service.cancel_shipment(shipment_id, customer_id, is_admin)
    except ShipmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ShipmentCannotBeCancelledException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UnauthorizedAccessException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
