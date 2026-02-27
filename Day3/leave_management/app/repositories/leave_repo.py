# leave_repo.py

from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.leave_request import LeaveRequest
from app.models.user import User
from datetime import date


# Create Leave Request
def create_leave(db: Session, leave_data: dict) -> LeaveRequest:
    db_leave = LeaveRequest(**leave_data)
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave


# Get Leave by ID
def get_leave_by_id(db: Session, leave_id: int) -> LeaveRequest:
    return db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()


# Get Leaves by Employee ID
def get_leaves_by_employee(db: Session, employee_id: int) -> list[LeaveRequest]:
    return db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id).all()


# Get All Leaves
def get_all_leaves(db: Session) -> list[LeaveRequest]:
    return db.query(LeaveRequest).all()


# Get All Leaves Query (for pagination)
def get_all_leaves_query(db: Session):
    return db.query(LeaveRequest)


# Get Leaves by Department
def get_leaves_by_department(db: Session, department_id: int) -> list[LeaveRequest]:
    return (
        db.query(LeaveRequest)
        .join(User, LeaveRequest.employee_id == User.id)
        .filter(User.department_id == department_id)
        .all()
    )


# Get Leaves by Department Query (for pagination)
def get_leaves_by_department_query(db: Session, department_id: int):
    return (
        db.query(LeaveRequest)
        .join(User, LeaveRequest.employee_id == User.id)
        .filter(User.department_id == department_id)
    )


# Get Leaves by Status
def get_leaves_by_status(db: Session, status: str) -> list[LeaveRequest]:
    return db.query(LeaveRequest).filter(LeaveRequest.status == status).all()


# Check for overlapping leaves
def check_overlapping_leave(
    db: Session, 
    employee_id: int, 
    start_date: date, 
    end_date: date,
    exclude_leave_id: int = None
) -> LeaveRequest:
    query = db.query(LeaveRequest).filter(
        LeaveRequest.employee_id == employee_id,
        LeaveRequest.status != "REJECTED",
        and_(
            LeaveRequest.start_date <= end_date,
            LeaveRequest.end_date >= start_date
        )
    )
    if exclude_leave_id:
        query = query.filter(LeaveRequest.id != exclude_leave_id)
    return query.first()


# Update Leave Status
def update_leave_status(db: Session, leave: LeaveRequest, status: str, approved_by: int) -> LeaveRequest:
    leave.status = status
    leave.approved_by = approved_by
    db.commit()
    db.refresh(leave)
    return leave


# Update Leave Request
def update_leave(db: Session, leave: LeaveRequest, update_data: dict) -> LeaveRequest:
    for key, value in update_data.items():
        if value is not None:
            setattr(leave, key, value)
    db.commit()
    db.refresh(leave)
    return leave


# Delete Leave Request
def delete_leave(db: Session, leave: LeaveRequest):
    db.delete(leave)
    db.commit()


# Get Leave Statistics
def get_leave_stats(db: Session) -> dict:
    total = db.query(LeaveRequest).count()
    pending = db.query(LeaveRequest).filter(LeaveRequest.status == "PENDING").count()
    approved = db.query(LeaveRequest).filter(LeaveRequest.status == "APPROVED").count()
    rejected = db.query(LeaveRequest).filter(LeaveRequest.status == "REJECTED").count()
    return {
        "total_leaves": total,
        "pending_leaves": pending,
        "approved_leaves": approved,
        "rejected_leaves": rejected
    }


# Get Department Leave Statistics
def get_department_leave_stats(db: Session, department_id: int) -> dict:
    base_query = (
        db.query(LeaveRequest)
        .join(User, LeaveRequest.employee_id == User.id)
        .filter(User.department_id == department_id)
    )
    total = base_query.count()
    pending = base_query.filter(LeaveRequest.status == "PENDING").count()
    approved = base_query.filter(LeaveRequest.status == "APPROVED").count()
    rejected = base_query.filter(LeaveRequest.status == "REJECTED").count()
    return {
        "total_leaves": total,
        "pending_leaves": pending,
        "approved_leaves": approved,
        "rejected_leaves": rejected
    }
