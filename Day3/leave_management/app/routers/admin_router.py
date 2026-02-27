# app/routers/admin_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import role_required
from app.controllers.admin_controller import AdminController
from app.schemas.user_schema import UserResponse, UserUpdate
from app.schemas.department_schema import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from app.schemas.leave_schema import LeaveApproval, LeaveStats
from app.core.pagination import paginate_params
from typing import List


router = APIRouter(prefix="/admin", tags=["Admin"])


# -----------------------------
# User Management
# -----------------------------

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.get_all_users(db)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.get_user(db, user_id)


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.update_user(db, user_id, update_data.dict(exclude_unset=True))


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.delete_user(db, user_id)


@router.put("/users/{user_id}/department/{department_id}", response_model=UserResponse)
def assign_user_to_department(
    user_id: int,
    department_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.assign_user_to_department(db, user_id, department_id)


# -----------------------------
# Department Management
# -----------------------------

@router.post("/departments", response_model=DepartmentResponse)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.create_department(db, department.dict())


@router.get("/departments", response_model=List[DepartmentResponse])
def get_all_departments(
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.get_all_departments(db)


@router.get("/departments/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.get_department(db, department_id)


@router.put("/departments/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    update_data: DepartmentUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.update_department(db, department_id, update_data.dict(exclude_unset=True))


@router.put("/departments/{department_id}/manager/{manager_id}", response_model=DepartmentResponse)
def assign_manager(
    department_id: int,
    manager_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.assign_manager(db, department_id, manager_id)


@router.delete("/departments/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.delete_department(db, department_id)


# -----------------------------
# Leave Management
# -----------------------------

@router.get("/leaves")
def get_all_leaves(
    pagination: dict = Depends(paginate_params),
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.get_all_leaves(db, pagination["page"], pagination["size"])


@router.put("/leaves/{leave_id}/status")
def override_leave_status(
    leave_id: int,
    approval: LeaveApproval,
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.override_leave(db, leave_id, user.id, approval.status)


# -----------------------------
# Reports
# -----------------------------

@router.get("/reports/leaves", response_model=LeaveStats)
def get_leave_stats(
    db: Session = Depends(get_db),
    user=Depends(role_required("ADMIN"))
):
    return AdminController.get_leave_stats(db)
