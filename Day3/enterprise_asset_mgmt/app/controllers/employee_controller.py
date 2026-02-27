from sqlalchemy.orm import Session
from app.services.request_service import RequestService
from app.services.assignment_service import AssignmentService
from app.schemas.request_schema import AssetRequestCreate

class EmployeeController:
    def __init__(self, db: Session):
        self.request_service = RequestService(db)
        self.assignment_service = AssignmentService(db)
    
    def create_request(self, employee_id: int, request_data: AssetRequestCreate):
        return self.request_service.create_request(employee_id, request_data)
    
    def get_user_requests(self, user_id: int, skip: int, limit: int):
        return self.request_service.get_user_requests(user_id, skip, limit)
    
    def get_user_assignments(self, user_id: int, skip: int, limit: int):
        return self.assignment_service.get_user_assignments(user_id, skip, limit)