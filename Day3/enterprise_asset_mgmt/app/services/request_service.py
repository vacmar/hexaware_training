from sqlalchemy.orm import Session
from app.repositories.request_repo import AssetRequestRepository
from app.repositories.asset_repo import AssetRepository
from app.services.assignment_service import AssignmentService
from app.schemas.request_schema import AssetRequestCreate
from app.schemas.assignment_schema import AssetAssignmentCreate
from fastapi import HTTPException

class RequestService:
    def __init__(self, db: Session):
        self.request_repo = AssetRequestRepository(db)
        self.asset_repo = AssetRepository(db)
        self.assignment_service = AssignmentService(db)
    
    def create_request(self, employee_id: int, request_data: AssetRequestCreate):
        return self.request_repo.create_request(employee_id, request_data)
    
    def get_user_requests(self, user_id: int, skip: int, limit: int):
        return self.request_repo.get_user_requests(user_id, skip, limit)
    
    def get_all_requests(self, skip: int, limit: int, status: str = None):
        return self.request_repo.get_all_requests(skip, limit, status)
    
    def approve_request(self, request_id: int, asset_id: int, approved_by: int):
        request = self.request_repo.get_request_by_id(request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        if request.status != "PENDING":
            raise HTTPException(status_code=400, detail="Request already processed")
        asset = self.asset_repo.get_asset_by_id(asset_id)
        if not asset or asset.status != "AVAILABLE":
            raise HTTPException(status_code=400, detail="Asset not available")
        self.request_repo.update_request_status(request_id, "APPROVED", approved_by)
        assignment_data = AssetAssignmentCreate(asset_id=asset_id, user_id=request.employee_id)
        self.assignment_service.assign_asset(assignment_data)
        return request
    
    def reject_request(self, request_id: int, approved_by: int):
        request = self.request_repo.get_request_by_id(request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        if request.status != "PENDING":
            raise HTTPException(status_code=400, detail="Request already processed")
        self.request_repo.update_request_status(request_id, "REJECTED", approved_by)
        return request
