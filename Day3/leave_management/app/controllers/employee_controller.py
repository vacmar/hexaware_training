from sqlalchemy.orm import Session
from app.services.leave_service import (
    apply_leave_service,
    get_employee_leaves_service,
    get_leave_by_id_service,
    cancel_leave_service
)


class EmployeeController:

    # -----------------------------
    # Leave Management
    # -----------------------------

    @staticmethod
    def apply_leave(db: Session, employee_id: int, leave_data: dict):
        return apply_leave_service(db, employee_id, leave_data)

    @staticmethod
    def get_my_leaves(db: Session, employee_id: int):
        return get_employee_leaves_service(db, employee_id)

    @staticmethod
    def get_leave_details(db: Session, leave_id: int, employee_id: int):
        leave = get_leave_by_id_service(db, leave_id)
        # Verify ownership
        if leave.employee_id != employee_id:
            from fastapi import HTTPException
            raise HTTPException(status_code=403, detail="You can only view your own leave requests")
        return leave

    @staticmethod
    def cancel_leave(db: Session, leave_id: int, employee_id: int):
        return cancel_leave_service(db, leave_id, employee_id)
