# app/routers/employee_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import role_required
from app.controllers.employee_controller import EmployeeController
from app.schemas.leave_schema import LeaveCreate, LeaveResponse
from typing import List


router = APIRouter(prefix="/employee", tags=["Employee"])


# -----------------------------
# Leave Management
# -----------------------------

@router.post("/leaves", response_model=LeaveResponse)
def apply_leave(
    leave_data: LeaveCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("EMPLOYEE"))
):
    return EmployeeController.apply_leave(db, user.id, leave_data.dict())


@router.get("/leaves", response_model=List[LeaveResponse])
def get_my_leaves(
    db: Session = Depends(get_db),
    user=Depends(role_required("EMPLOYEE"))
):
    return EmployeeController.get_my_leaves(db, user.id)


@router.get("/leaves/{leave_id}", response_model=LeaveResponse)
def get_leave_details(
    leave_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("EMPLOYEE"))
):
    return EmployeeController.get_leave_details(db, leave_id, user.id)


@router.delete("/leaves/{leave_id}")
def cancel_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("EMPLOYEE"))
):
    return EmployeeController.cancel_leave(db, leave_id, user.id)
