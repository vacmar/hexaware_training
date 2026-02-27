from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import require_roles
from app.core.pagination import PaginatedResponse, get_pagination_params
from app.schemas.request_schema import AssetRequestCreate, AssetRequestResponse
from app.schemas.assignment_schema import AssetAssignmentResponse
from app.controllers.employee_controller import EmployeeController
from app.models.user import User

router = APIRouter(prefix="/employee", tags=["Employee"])

@router.post("/requests", response_model=AssetRequestResponse)
def create_request(request_data: AssetRequestCreate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("EMPLOYEE", "MANAGER", "IT_ADMIN", "SUPERADMIN"))):
    controller = EmployeeController(db)
    return controller.create_request(current_user.id, request_data)

@router.get("/requests", response_model=PaginatedResponse[AssetRequestResponse])
def get_my_requests(page: int = 1, page_size: int = 10, db: Session = Depends(get_db), current_user: User = Depends(require_roles("EMPLOYEE", "MANAGER", "IT_ADMIN", "SUPERADMIN"))):
    skip, limit = get_pagination_params(page, page_size)
    controller = EmployeeController(db)
    requests, total = controller.get_user_requests(current_user.id, skip, limit)
    return {"total": total, "page": page, "page_size": page_size, "data": requests}

@router.get("/assignments", response_model=PaginatedResponse[AssetAssignmentResponse])
def get_my_assignments(page: int = 1, page_size: int = 10, db: Session = Depends(get_db), current_user: User = Depends(require_roles("EMPLOYEE", "MANAGER", "IT_ADMIN", "SUPERADMIN"))):
    skip, limit = get_pagination_params(page, page_size)
    controller = EmployeeController(db)
    assignments, total = controller.get_user_assignments(current_user.id, skip, limit)
    return {"total": total, "page": page, "page_size": page_size, "data": assignments}
