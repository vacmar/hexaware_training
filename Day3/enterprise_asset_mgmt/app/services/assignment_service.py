from sqlalchemy.orm import Session
from app.repositories.assignment_repo import AssetAssignmentRepository
from app.repositories.asset_repo import AssetRepository
from app.schemas.assignment_schema import AssetAssignmentCreate
from app.schemas.asset_schema import AssetUpdate
from fastapi import HTTPException

class AssignmentService:
    def __init__(self, db: Session):
        self.assignment_repo = AssetAssignmentRepository(db)
        self.asset_repo = AssetRepository(db)
    
    def assign_asset(self, assignment_data: AssetAssignmentCreate):
        asset = self.asset_repo.get_asset_by_id(assignment_data.asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        if asset.status != "AVAILABLE":
            raise HTTPException(status_code=400, detail="Asset is not available")
        active_assignment = self.assignment_repo.get_active_assignment_by_asset(assignment_data.asset_id)
        if active_assignment:
            raise HTTPException(status_code=400, detail="Asset is already assigned")
        assignment = self.assignment_repo.create_assignment(assignment_data)
        asset_update = AssetUpdate(status="ASSIGNED")
        self.asset_repo.update_asset(assignment_data.asset_id, asset_update)
        return assignment
    
    def return_asset(self, assignment_id: int, condition: str):
        assignment = self.assignment_repo.get_assignment_by_id(assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        if assignment.returned_date:
            raise HTTPException(status_code=400, detail="Asset already returned")
        self.assignment_repo.return_asset(assignment_id, condition)
        asset_update = AssetUpdate(status="AVAILABLE")
        self.asset_repo.update_asset(assignment.asset_id, asset_update)
        return assignment
    
    def get_user_assignments(self, user_id: int, skip: int, limit: int):
        return self.assignment_repo.get_user_assignments(user_id, skip, limit)
    
    def get_all_assignments(self, skip: int, limit: int):
        return self.assignment_repo.get_all_assignments(skip, limit)
