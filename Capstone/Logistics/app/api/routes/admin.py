"""
Admin routes
"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.dependencies import require_admin
from ...models.user import User, UserRole
from ...services.user_service import UserService
from ...services.shipment_service import ShipmentService
from ...services.hub_service import HubService
from ...schemas.user_schema import UserResponse, UserListResponse, UserUpdate
from ...schemas.hub_schema import AdminReportResponse

router = APIRouter()


@router.get("/users", response_model=UserListResponse)
def get_all_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    role: Optional[UserRole] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Get all users.
    
    Admin only.
    """
    service = UserService(db)
    skip = (page - 1) * page_size
    users, total = service.get_all_users(skip, page_size, role)
    
    return UserListResponse(
        users=users,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Get user details by ID.
    
    Admin only.
    """
    service = UserService(db)
    user = service.get_user(user_id)
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update a user.
    
    Admin only.
    """
    service = UserService(db)
    user = service.update_user(user_id, update_data)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete a user.
    
    Admin only.
    """
    service = UserService(db)
    service.delete_user(user_id)
    return {"message": "User deleted successfully"}


@router.get("/agents", response_model=list[UserResponse])
def get_agents(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Get all delivery agents.
    
    Admin only.
    """
    service = UserService(db)
    agents = service.get_agents()
    return agents


@router.get("/reports", response_model=AdminReportResponse)
def get_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Get administrative reports and statistics.
    
    Admin only.
    """
    shipment_service = ShipmentService(db)
    user_service = UserService(db)
    hub_service = HubService(db)
    
    # Get shipment stats
    shipment_stats = shipment_service.get_shipment_stats()
    
    # Get user counts
    user_counts = user_service.count_by_role()
    
    # Get hub count
    hub_count = hub_service.get_hub_count()
    
    return AdminReportResponse(
        total_shipments_today=shipment_stats["total_shipments_today"],
        delivered=shipment_stats["delivered"],
        in_transit=shipment_stats["in_transit"],
        out_for_delivery=shipment_stats["out_for_delivery"],
        created=shipment_stats["created"],
        cancelled=shipment_stats["cancelled"],
        total_users=user_counts["total"],
        total_customers=user_counts["customers"],
        total_agents=user_counts["agents"],
        total_hubs=hub_count
    )
