"""
Hub routes
"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.dependencies import require_admin
from ...models.user import User
from ...services.hub_service import HubService
from ...schemas.hub_schema import (
    HubCreate,
    HubUpdate,
    HubResponse,
    HubListResponse
)

router = APIRouter()


@router.get("", response_model=HubListResponse)
def get_hubs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    active_only: bool = Query(False),
    city: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all hubs.
    
    Public endpoint - no authentication required.
    """
    service = HubService(db)
    
    if city:
        hubs = service.get_hubs_by_city(city)
        total = len(hubs)
    else:
        skip = (page - 1) * page_size
        hubs, total = service.get_all_hubs(skip, page_size, active_only)
    
    return HubListResponse(
        hubs=hubs,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{hub_id}", response_model=HubResponse)
def get_hub(hub_id: UUID, db: Session = Depends(get_db)):
    """
    Get hub details by ID.
    
    Public endpoint.
    """
    service = HubService(db)
    hub = service.get_hub(hub_id)
    return hub


@router.post("", response_model=HubResponse, status_code=status.HTTP_201_CREATED)
def create_hub(
    hub_data: HubCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create a new hub.
    
    Admin only.
    """
    service = HubService(db)
    hub = service.create_hub(hub_data)
    return hub


@router.put("/{hub_id}", response_model=HubResponse)
def update_hub(
    hub_id: UUID,
    update_data: HubUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update a hub.
    
    Admin only.
    """
    service = HubService(db)
    hub = service.update_hub(hub_id, update_data)
    return hub


@router.delete("/{hub_id}", status_code=status.HTTP_200_OK)
def delete_hub(
    hub_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete a hub.
    
    Admin only.
    """
    service = HubService(db)
    service.delete_hub(hub_id)
    return {"message": "Hub deleted successfully"}
