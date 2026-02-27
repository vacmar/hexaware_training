from sqlalchemy.orm import Session
from app.services.asset_service import AssetService
from app.services.assignment_service import AssignmentService
from app.services.request_service import RequestService
from app.schemas.asset_schema import AssetCreate, AssetUpdate
from app.schemas.assignment_schema import AssetAssignmentCreate

class ITAdminController:
    def __init__(self, db: Session):
        self.asset_service = AssetService(db)
        self.assignment_service = AssignmentService(db)
        self.request_service = RequestService(db)
    
    def create_asset(self, asset_data: AssetCreate):
        return self.asset_service.create_asset(asset_data)
    
    def get_all_assets(self, skip: int, limit: int, status: str = None, asset_type: str = None):
        return self.asset_service.get_all_assets(skip, limit, status, asset_type)
    
    def update_asset(self, asset_id: int, asset_data: AssetUpdate):
        return self.asset_service.update_asset(asset_id, asset_data)
    
    def delete_asset(self, asset_id: int):
        return self.asset_service.delete_asset(asset_id)
    
    def assign_asset(self, assignment_data: AssetAssignmentCreate):
        return self.assignment_service.assign_asset(assignment_data)
    
    def return_asset(self, assignment_id: int, condition: str):
        return self.assignment_service.return_asset(assignment_id, condition)
    
    def get_all_assignments(self, skip: int, limit: int):
        return self.assignment_service.get_all_assignments(skip, limit)
    
    def get_all_requests(self, skip: int, limit: int, status: str = None):
        return self.request_service.get_all_requests(skip, limit, status)
    
    def approve_request(self, request_id: int, asset_id: int, approved_by: int):
        return self.request_service.approve_request(request_id, asset_id, approved_by)
    
    def reject_request(self, request_id: int, approved_by: int):
        return self.request_service.reject_request(request_id, approved_by)