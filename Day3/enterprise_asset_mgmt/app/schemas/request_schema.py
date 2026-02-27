from pydantic import BaseModel, ConfigDict
from typing import Optional

class AssetRequestBase(BaseModel):
    asset_type: str
    reason: Optional[str] = None

class AssetRequestCreate(AssetRequestBase):
    pass

class AssetRequestUpdate(BaseModel):
    status: Optional[str] = None
    approved_by: Optional[int] = None

class AssetRequestResponse(AssetRequestBase):
    id: int
    employee_id: int
    status: str
    approved_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
