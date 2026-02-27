from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date
from app.repositories.leave_repo import (
    create_leave,
    get_leave_by_id,
    get_leaves_by_employee,
    get_all_leaves,
    get_all_leaves_query,
    get_leaves_by_department,
    get_leaves_by_department_query,
    check_overlapping_leave,
    update_leave_status,
    update_leave,
    delete_leave,
    get_leave_stats,
    get_department_leave_stats
)
from app.repositories.user_repo import get_user_by_id
from app.repositories.department_repo import get_department_by_id, get_department_by_manager
from app.core.pagination import paginate_query


# -----------------------------
# Apply for Leave (Employee)
# -----------------------------

def apply_leave_service(db: Session, employee_id: int, leave_data: dict):
    # Validate employee exists
    employee = get_user_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Validate dates
    start_date = leave_data["start_date"]
    end_date = leave_data["end_date"]
    
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date must be before or equal to end date")
    
    if start_date < date.today():
        raise HTTPException(status_code=400, detail="Cannot apply leave for past dates")
    
    # Check for overlapping leaves
    overlap = check_overlapping_leave(db, employee_id, start_date, end_date)
    if overlap:
        raise HTTPException(status_code=400, detail="Overlapping leave request exists")
    
    leave_data["employee_id"] = employee_id
    leave_data["status"] = "PENDING"
    
    return create_leave(db, leave_data)


# -----------------------------
# Get Employee Leaves
# -----------------------------

def get_employee_leaves_service(db: Session, employee_id: int):
    return get_leaves_by_employee(db, employee_id)


# -----------------------------
# Get Leave by ID
# -----------------------------

def get_leave_by_id_service(db: Session, leave_id: int):
    leave = get_leave_by_id(db, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return leave


# -----------------------------
# Get All Leaves (Admin) with Pagination
# -----------------------------

def list_all_leaves_service(db: Session, page: int, size: int):
    query = get_all_leaves_query(db)
    return paginate_query(query, page, size)


# -----------------------------
# Get Department Leaves (Manager) with Pagination
# -----------------------------

def list_department_leaves_service(db: Session, manager_id: int, page: int, size: int):
    # Get manager's department
    department = get_department_by_manager(db, manager_id)
    if not department:
        raise HTTPException(status_code=404, detail="You are not assigned to any department")
    
    query = get_leaves_by_department_query(db, department.id)
    return paginate_query(query, page, size)


# -----------------------------
# Approve/Reject Leave (Manager)
# -----------------------------

def process_leave_service(db: Session, leave_id: int, manager_id: int, status: str):
    leave = get_leave_by_id(db, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    if leave.status != "PENDING":
        raise HTTPException(status_code=400, detail="Leave request is not pending")
    
    # Validate status
    if status not in ["APPROVED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="Status must be APPROVED or REJECTED")
    
    # Get manager's department
    manager_dept = get_department_by_manager(db, manager_id)
    if not manager_dept:
        raise HTTPException(status_code=403, detail="You are not assigned to any department")
    
    # Verify leave belongs to manager's department
    employee = get_user_by_id(db, leave.employee_id)
    if employee.department_id != manager_dept.id:
        raise HTTPException(status_code=403, detail="Leave request does not belong to your department")
    
    return update_leave_status(db, leave, status, manager_id)


# -----------------------------
# Override Leave Status (Admin)
# -----------------------------

def override_leave_service(db: Session, leave_id: int, admin_id: int, status: str):
    leave = get_leave_by_id(db, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    # Validate status
    if status not in ["PENDING", "APPROVED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="Status must be PENDING, APPROVED, or REJECTED")
    
    return update_leave_status(db, leave, status, admin_id)


# -----------------------------
# Cancel Leave (Employee)
# -----------------------------

def cancel_leave_service(db: Session, leave_id: int, employee_id: int):
    leave = get_leave_by_id(db, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    if leave.employee_id != employee_id:
        raise HTTPException(status_code=403, detail="You can only cancel your own leave requests")
    
    if leave.status != "PENDING":
        raise HTTPException(status_code=400, detail="Can only cancel pending leave requests")
    
    delete_leave(db, leave)
    return {"message": "Leave request cancelled successfully"}


# -----------------------------
# Get Company-wide Leave Stats (Admin)
# -----------------------------

def get_company_leave_stats_service(db: Session):
    return get_leave_stats(db)


# -----------------------------
# Get Department Leave Stats (Manager)
# -----------------------------

def get_department_leave_stats_service(db: Session, manager_id: int):
    department = get_department_by_manager(db, manager_id)
    if not department:
        raise HTTPException(status_code=404, detail="You are not assigned to any department")
    
    stats = get_department_leave_stats(db, department.id)
    stats["department_id"] = department.id
    stats["department_name"] = department.name
    return stats
