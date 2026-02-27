from sqlalchemy.orm import Session
from app.services.user_service import (
    get_all_users_service,
    get_user_by_id_service,
    update_user_service,
    delete_user_service,
    assign_user_to_department_service
)
from app.services.department_service import (
    create_department_service,
    get_all_departments_service,
    get_department_by_id_service,
    update_department_service,
    assign_manager_service,
    delete_department_service
)
from app.services.leave_service import (
    list_all_leaves_service,
    override_leave_service,
    get_company_leave_stats_service
)


class AdminController:

    # -----------------------------
    # User Management
    # -----------------------------

    @staticmethod
    def get_all_users(db: Session):
        return get_all_users_service(db)

    @staticmethod
    def get_user(db: Session, user_id: int):
        return get_user_by_id_service(db, user_id)

    @staticmethod
    def update_user(db: Session, user_id: int, data: dict):
        return update_user_service(db, user_id, data)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        return delete_user_service(db, user_id)

    @staticmethod
    def assign_user_to_department(db: Session, user_id: int, department_id: int):
        return assign_user_to_department_service(db, user_id, department_id)

    # -----------------------------
    # Department Management
    # -----------------------------

    @staticmethod
    def create_department(db: Session, data: dict):
        return create_department_service(db, data)

    @staticmethod
    def get_all_departments(db: Session):
        return get_all_departments_service(db)

    @staticmethod
    def get_department(db: Session, department_id: int):
        return get_department_by_id_service(db, department_id)

    @staticmethod
    def update_department(db: Session, department_id: int, data: dict):
        return update_department_service(db, department_id, data)

    @staticmethod
    def assign_manager(db: Session, department_id: int, manager_id: int):
        return assign_manager_service(db, department_id, manager_id)

    @staticmethod
    def delete_department(db: Session, department_id: int):
        return delete_department_service(db, department_id)

    # -----------------------------
    # Leave Management
    # -----------------------------

    @staticmethod
    def get_all_leaves(db: Session, page: int, size: int):
        return list_all_leaves_service(db, page, size)

    @staticmethod
    def override_leave(db: Session, leave_id: int, admin_id: int, status: str):
        return override_leave_service(db, leave_id, admin_id, status)

    # -----------------------------
    # Reports
    # -----------------------------

    @staticmethod
    def get_leave_stats(db: Session):
        return get_company_leave_stats_service(db)
