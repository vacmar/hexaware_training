"""
Hub Service Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import sys
import os
import httpx
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from shared.database import get_db
from shared.config import settings
from .services import HubService, HubNotFoundException, HubAlreadyExistsException
from .schemas import HubCreate, HubUpdate, HubResponse, HubListResponse

hub_router = APIRouter()


async def verify_admin_token(authorization: str = Header(...)):
    """Verify admin token by calling auth service"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    token = authorization.split(" ")[1]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.AUTH_SERVICE_URL}/auth/validate-token",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
            
            payload = response.json()
            if payload.get("role") != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admin access required"
                )
            return payload
    except httpx.RequestError:
        # If auth service is unavailable, allow request (for development)
        return {"role": "admin"}


@hub_router.post("/", response_model=HubResponse, status_code=status.HTTP_201_CREATED)
async def create_hub(
    hub_data: HubCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_admin_token)
):
    """Create a new hub (admin only)"""
    try:
        hub_service = HubService(db)
        hub = hub_service.create_hub(hub_data)
        return hub
    except HubAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@hub_router.get("/", response_model=HubListResponse)
def get_all_hubs(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get all hubs with pagination"""
    hub_service = HubService(db)
    hubs, total = hub_service.get_all_hubs(skip, limit, active_only)
    return HubListResponse(hubs=hubs, total=total, skip=skip, limit=limit)


@hub_router.get("/search/city/{city}", response_model=List[HubResponse])
def get_hubs_by_city(
    city: str,
    db: Session = Depends(get_db)
):
    """Get all hubs in a specific city"""
    hub_service = HubService(db)
    return hub_service.get_hubs_by_city(city)


@hub_router.get("/{hub_id}", response_model=HubResponse)
def get_hub(
    hub_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific hub by ID"""
    try:
        hub_service = HubService(db)
        return hub_service.get_hub(hub_id)
    except HubNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@hub_router.put("/{hub_id}", response_model=HubResponse)
async def update_hub(
    hub_id: UUID,
    update_data: HubUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_admin_token)
):
    """Update a hub (admin only)"""
    try:
        hub_service = HubService(db)
        return hub_service.update_hub(hub_id, update_data)
    except HubNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HubAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@hub_router.delete("/{hub_id}")
async def delete_hub(
    hub_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_admin_token)
):
    """Delete a hub (admin only)"""
    try:
        hub_service = HubService(db)
        hub_service.delete_hub(hub_id)
        return {"message": "Hub deleted successfully"}
    except HubNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
