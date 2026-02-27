from sqlalchemy.orm import Session
from app.services.asset_service import AssetService
from app.services.assignment_service import AssignmentService

class ManagerController:
    def __init__(self, db: Session):
        self.asset_service = AssetService(db)
        self.assignment_service = AssignmentService(db)
    
    def get_department_assets(self, dept_id: int, skip: int, limit: int):
        return self.asset_service.get_department_assets(dept_id, skip, limit)
    
    def get_user_assignments(self, user_id: int, skip: int, limit: int):
        return self.assignment_service.get_user_assignments(user_id, skip, limit)