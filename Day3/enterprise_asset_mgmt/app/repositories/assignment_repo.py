from sqlalchemy.orm import Session
from app.models.asset_assignment import AssetAssignment
from app.schemas.assignment_schema import AssetAssignmentCreate
from typing import Optional, List
from datetime import date

class AssetAssignmentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_assignment(self, assignment_data: AssetAssignmentCreate) -> AssetAssignment:
        assignment = AssetAssignment(
            asset_id=assignment_data.asset_id,
            user_id=assignment_data.user_id,
            assigned_date=date.today()
        )
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment
    
    def get_assignment_by_id(self, assignment_id: int) -> Optional[AssetAssignment]:
        return self.db.query(AssetAssignment).filter(AssetAssignment.id == assignment_id).first()
    
    def get_active_assignment_by_asset(self, asset_id: int) -> Optional[AssetAssignment]:
        return self.db.query(AssetAssignment).filter(
            AssetAssignment.asset_id == asset_id,
            AssetAssignment.returned_date == None
        ).first()
    
    def get_user_assignments(self, user_id: int, skip: int = 0, limit: int = 10) -> tuple[List[AssetAssignment], int]:
        query = self.db.query(AssetAssignment).filter(AssetAssignment.user_id == user_id)
        total = query.count()
        assignments = query.offset(skip).limit(limit).all()
        return assignments, total
    
    def get_all_assignments(self, skip: int = 0, limit: int = 10) -> tuple[List[AssetAssignment], int]:
        query = self.db.query(AssetAssignment)
        total = query.count()
        assignments = query.offset(skip).limit(limit).all()
        return assignments, total
    
    def return_asset(self, assignment_id: int, condition: Optional[str] = None) -> Optional[AssetAssignment]:
        assignment = self.get_assignment_by_id(assignment_id)
        if assignment and not assignment.returned_date:
            assignment.returned_date = date.today()
            assignment.condition_on_return = condition
            self.db.commit()
            self.db.refresh(assignment)
        return assignment