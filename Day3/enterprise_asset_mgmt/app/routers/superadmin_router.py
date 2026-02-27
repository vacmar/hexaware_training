from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import require_roles
from app.core.pagination import PaginatedResponse, get_pagination_params
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.schemas.asset_schema import AssetCreate, AssetUpdate, AssetResponse
from app.controllers.superadmin_controller import SuperAdminController
from app.models.user import User

router = APIRouter(prefix="/superadmin", tags=["SuperAdmin"])

@router.post("/users", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("SUPERADMIN"))):
    controller = SuperAdminController(db)
    return controller.create_user(user_data)

@router.get("/users", response_model=PaginatedResponse[UserResponse])
def get_all_users(page: int = 1, page_size: int = 10, db: Session = Depends(get_db), current_user: User = Depends(require_roles("SUPERADMIN"))):
    skip, limit = get_pagination_params(page, page_size)
    controller = SuperAdminController(db)
    users, total = controller.get_all_users(skip, limit)
    return {"total": total, "page": page, "page_size": page_size, "data": users}

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("SUPERADMIN"))):
    controller = SuperAdminController(db)
    return controller.update_user(user_id, user_data)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles("SUPERADMIN"))):
    controller = SuperAdminController(db)
    controller.delete_user(user_id)
    return {"message": "User deleted successfully"}

@router.post("/departments", response_model=DepartmentResponse)
def create_department(dept_data: DepartmentCreate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("SUPERADMIN"))):
    controller = SuperAdminController(db)
    return controller.create_department(dept_data)

@router.get("/departments", response_model=PaginatedResponse[DepartmentResponse])
def get_all_departments(page: int = 1, page_size: int = 10, db: Session = Depends(get_db), current_user: User = Depends(require_roles("SUPERADMIN"))):
    skip, limit = get_pagination_params(page, page_size)
    controller = SuperAdminController(db)
    departments, total = controller.get_all_departments(skip, limit)
    return {"total": total, "page": page, "page_size": page_size, "data": departments}

@router.post("/assets", response_model=AssetResponse)
def create_asset(asset_data: AssetCreate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("SUPERADMIN"))):
    controller = SuperAdminController(db)
    return controller.create_asset(asset_data)

@router.get("/assets", response_model=PaginatedResponse[AssetResponse])
def get_all_assets(page: int = 1, page_size: int = 10, status: str = None, asset_type: str = None, db: Session = Depends(get_db), current_user: User = Depends(require_roles("SUPERADMIN"))):
    skip, limit = get_pagination_params(page, page_size)
    controller = SuperAdminController(db)
    assets, total = controller.get_all_assets(skip, limit, status, asset_type)
    return {"total": total, "page": page, "page_size": page_size, "data": assets}
