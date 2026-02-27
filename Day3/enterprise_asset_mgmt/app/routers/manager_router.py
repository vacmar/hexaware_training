from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import require_roles
from app.core.pagination import PaginatedResponse, get_pagination_params
from app.schemas.asset_schema import AssetResponse
from app.schemas.assignment_schema import AssetAssignmentResponse
from app.controllers.manager_controller import ManagerController
from app.models.user import User

router = APIRouter(prefix="/manager", tags=["Manager"])

@router.get("/department-assets", response_model=PaginatedResponse[AssetResponse])
def get_department_assets(page: int = 1, page_size: int = 10, db: Session = Depends(get_db), current_user: User = Depends(require_roles("MANAGER", "IT_ADMIN", "SUPERADMIN"))):
    if not current_user.department_id:
        return {"total": 0, "page": page, "page_size": page_size, "data": []}
    skip, limit = get_pagination_params(page, page_size)
    controller = ManagerController(db)
    assets, total = controller.get_department_assets(current_user.department_id, skip, limit)
    return {"total": total, "page": page, "page_size": page_size, "data": assets}

@router.get("/my-assets", response_model=PaginatedResponse[AssetAssignmentResponse])
def get_my_assets(page: int = 1, page_size: int = 10, db: Session = Depends(get_db), current_user: User = Depends(require_roles("MANAGER", "IT_ADMIN", "SUPERADMIN"))):
    skip, limit = get_pagination_params(page, page_size)
    controller = ManagerController(db)
    assignments, total = controller.get_user_assignments(current_user.id, skip, limit)
    return {"total": total, "page": page, "page_size": page_size, "data": assignments}
