from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class AssetAssignmentBase(BaseModel):
    asset_id: int
    user_id: int

class AssetAssignmentCreate(AssetAssignmentBase):
    assigned_date: date

class AssetReturnRequest(BaseModel):
    returned_date: date
    condition_on_return: Optional[str] = None

class AssetAssignmentResponse(AssetAssignmentBase):
    id: int
    assigned_date: date
    returned_date: Optional[date] = None
    condition_on_return: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
