# app/routers/manager_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import role_required
from app.controllers.manager_controller import ManagerController
from app.schemas.user_schema import UserResponse
from app.schemas.leave_schema import LeaveResponse, DepartmentLeaveStats
from app.core.pagination import paginate_params
from typing import List


router = APIRouter(prefix="/manager", tags=["Manager"])


# -----------------------------
# Department Employees
# -----------------------------

@router.get("/employees", response_model=List[UserResponse])
def get_department_employees(
    db: Session = Depends(get_db),
    user=Depends(role_required("MANAGER"))
):
    return ManagerController.get_department_employees(db, user.id)


# -----------------------------
# Leave Management
# -----------------------------

@router.get("/leaves")
def get_department_leaves(
    pagination: dict = Depends(paginate_params),
    db: Session = Depends(get_db),
    user=Depends(role_required("MANAGER"))
):
    return ManagerController.get_department_leaves(db, user.id, pagination["page"], pagination["size"])


@router.put("/leaves/{leave_id}/approve", response_model=LeaveResponse)
def approve_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("MANAGER"))
):
    return ManagerController.approve_leave(db, leave_id, user.id)


@router.put("/leaves/{leave_id}/reject", response_model=LeaveResponse)
def reject_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("MANAGER"))
):
    return ManagerController.reject_leave(db, leave_id, user.id)


# -----------------------------
# Reports
# -----------------------------

@router.get("/reports/leaves", response_model=DepartmentLeaveStats)
def get_leave_stats(
    db: Session = Depends(get_db),
    user=Depends(role_required("MANAGER"))
):
    return ManagerController.get_leave_stats(db, user.id)
