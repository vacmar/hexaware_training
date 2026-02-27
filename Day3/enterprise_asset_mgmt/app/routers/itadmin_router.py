from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import require_roles
from app.core.pagination import PaginatedResponse, get_pagination_params
from app.schemas.asset_schema import AssetCreate, AssetUpdate, AssetResponse
from app.schemas.assignment_schema import AssetAssignmentCreate, AssetAssignmentResponse, AssetReturnRequest
from app.schemas.request_schema import AssetRequestResponse
from app.controllers.itadmin_controller import ITAdminController
from app.models.user import User

router = APIRouter(prefix="/itadmin", tags=["IT Admin"])

@router.post("/assets", response_model=AssetResponse)
def create_asset(asset_data: AssetCreate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("IT_ADMIN", "SUPERADMIN"))):
    controller = ITAdminController(db)
    return controller.create_asset(asset_data)

@router.get("/assets", response_model=PaginatedResponse[AssetResponse])
def get_all_assets(page: int = 1, page_size: int = 10, status: str = None, asset_type: str = None, db: Session = Depends(get_db), current_user: User = Depends(require_roles("IT_ADMIN", "SUPERADMIN"))):
    skip, limit = get_pagination_params(page, page_size)
    controller = ITAdminController(db)
    assets, total = controller.get_all_assets(skip, limit, status, asset_type)
    return {"total": total, "page": page, "page_size": page_size, "data": assets}

@router.put("/assets/{asset_id}", response_model=AssetResponse)
def update_asset(asset_id: int, asset_data: AssetUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("IT_ADMIN", "SUPERADMIN"))):
    controller = ITAdminController(db)
    return controller.update_asset(asset_id, asset_data)

@router.delete("/assets/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles("IT_ADMIN", "SUPERADMIN"))):
    controller = ITAdminController(db)
    return controller.delete_asset(asset_id)

@router.post("/assignments", response_model=AssetAssignmentResponse)
def assign_asset(assignment_data: AssetAssignmentCreate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("IT_ADMIN", "SUPERADMIN"))):
    controller = ITAdminController(db)
    return controller.assign_asset(assignment_data)

@router.post("/assignments/{assignment_id}/return", response_model=AssetAssignmentResponse)
def return_asset(assignment_id: int, return_data: AssetReturnRequest, db: Session = Depends(get_db), current_user: User = Depends(require_roles("IT_ADMIN", "SUPERADMIN"))):
    controller = ITAdminController(db)
    return controller.return_asset(assignment_id, return_data.condition_on_return)

@router.get("/assignments", response_model=PaginatedResponse[AssetAssignmentResponse])
def get_all_assignments(page: int = 1, page_size: int = 10, db: Session = Depends(get_db), current_user: User = Depends(require_roles("IT_ADMIN", "SUPERADMIN"))):
    skip, limit = get_pagination_params(page, page_size)
    controller = ITAdminController(db)
    assignments, total = controller.get_all_assignments(skip, limit)
    return {"total": total, "page": page, "page_size": page_size, "data": assignments}

@router.get("/requests", response_model=PaginatedResponse[AssetRequestResponse])
def get_all_requests(page: int = 1, page_size: int = 10, status: str = None, db: Session = Depends(get_db), current_user: User = Depends(require_roles("IT_ADMIN", "SUPERADMIN"))):
    skip, limit = get_pagination_params(page, page_size)
    controller = ITAdminController(db)
    requests, total = controller.get_all_requests(skip, limit, status)
    return {"total": total, "page": page, "page_size": page_size, "data": requests}

@router.post("/requests/{request_id}/approve")
def approve_request(request_id: int, asset_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles("IT_ADMIN", "SUPERADMIN"))):
    controller = ITAdminController(db)
    return controller.approve_request(request_id, asset_id, current_user.id)

@router.post("/requests/{request_id}/reject")
def reject_request(request_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles("IT_ADMIN", "SUPERADMIN"))):
    controller = ITAdminController(db)
    return controller.reject_request(request_id, current_user.id)
    skip, limit = get_pagination_params(page, page_size)
    repo = MaintenanceRepository(db)
    records, total = repo.get_records_by_asset(asset_id, skip, limit)
    return {"total": total, "page": page, "page_size": page_size, "data": records}
