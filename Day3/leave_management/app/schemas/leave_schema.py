from pydantic import BaseModel
from typing import Optional
from datetime import date


class LeaveBase(BaseModel):
    start_date: date
    end_date: date
    reason: str


class LeaveCreate(LeaveBase):
    pass


class LeaveUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None


class LeaveResponse(LeaveBase):
    id: int
    employee_id: int
    status: str
    approved_by: Optional[int] = None

    class Config:
        from_attributes = True


class LeaveWithDetails(LeaveResponse):
    employee_name: Optional[str] = None
    approver_name: Optional[str] = None


class LeaveApproval(BaseModel):
    status: str  # APPROVED / REJECTED


class LeaveStats(BaseModel):
    total_leaves: int
    pending_leaves: int
    approved_leaves: int
    rejected_leaves: int


class DepartmentLeaveStats(LeaveStats):
    department_id: int
    department_name: str
