from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class AssetBase(BaseModel):
    asset_tag: str
    asset_type: str
    brand: Optional[str] = None
    model: Optional[str] = None

class AssetCreate(AssetBase):
    purchase_date: Optional[date] = None
    department_id: Optional[int] = None

class AssetUpdate(BaseModel):
    asset_tag: Optional[str] = None
    asset_type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    purchase_date: Optional[date] = None
    status: Optional[str] = None
    department_id: Optional[int] = None

class AssetResponse(AssetBase):
    id: int
    purchase_date: Optional[date] = None
    status: str
    department_id: Optional[int] = None
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
