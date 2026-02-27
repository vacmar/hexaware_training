from sqlalchemy.orm import Session
from app.models.asset_request import AssetRequest
from app.schemas.request_schema import AssetRequestCreate
from typing import Optional, List

class AssetRequestRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_request(self, employee_id: int, request_data: AssetRequestCreate) -> AssetRequest:
        request = AssetRequest(
            employee_id=employee_id,
            asset_type=request_data.asset_type,
            reason=request_data.reason
        )
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        return request
    
    def get_request_by_id(self, request_id: int) -> Optional[AssetRequest]:
        return self.db.query(AssetRequest).filter(AssetRequest.id == request_id).first()
    
    def get_user_requests(self, user_id: int, skip: int = 0, limit: int = 10) -> tuple[List[AssetRequest], int]:
        query = self.db.query(AssetRequest).filter(AssetRequest.employee_id == user_id)
        total = query.count()
        requests = query.offset(skip).limit(limit).all()
        return requests, total
    
    def get_all_requests(self, skip: int = 0, limit: int = 10, status: Optional[str] = None) -> tuple[List[AssetRequest], int]:
        query = self.db.query(AssetRequest)
        if status:
            query = query.filter(AssetRequest.status == status)
        total = query.count()
        requests = query.offset(skip).limit(limit).all()
        return requests, total
    
    def update_request_status(self, request_id: int, status: str, approved_by: Optional[int] = None) -> Optional[AssetRequest]:
        request = self.get_request_by_id(request_id)
        if request:
            request.status = status
            if approved_by:
                request.approved_by = approved_by
            self.db.commit()
            self.db.refresh(request)
        return request