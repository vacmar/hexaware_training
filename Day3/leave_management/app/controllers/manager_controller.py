from sqlalchemy.orm import Session
from app.services.user_service import get_department_employees_service
from app.services.leave_service import (
    list_department_leaves_service,
    process_leave_service,
    get_department_leave_stats_service
)
from app.repositories.department_repo import get_department_by_manager


class ManagerController:

    # -----------------------------
    # Department Employees
    # -----------------------------

    @staticmethod
    def get_department_employees(db: Session, manager_id: int):
        department = get_department_by_manager(db, manager_id)
        if not department:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="You are not assigned to any department")
        return get_department_employees_service(db, department.id)

    # -----------------------------
    # Leave Management
    # -----------------------------

    @staticmethod
    def get_department_leaves(db: Session, manager_id: int, page: int, size: int):
        return list_department_leaves_service(db, manager_id, page, size)

    @staticmethod
    def approve_leave(db: Session, leave_id: int, manager_id: int):
        return process_leave_service(db, leave_id, manager_id, "APPROVED")

    @staticmethod
    def reject_leave(db: Session, leave_id: int, manager_id: int):
        return process_leave_service(db, leave_id, manager_id, "REJECTED")

    # -----------------------------
    # Reports
    # -----------------------------

    @staticmethod
    def get_leave_stats(db: Session, manager_id: int):
        return get_department_leave_stats_service(db, manager_id)
