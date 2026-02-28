"""
Hub schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class HubBase(BaseModel):
    """Base hub schema"""
    hub_name: str
    city: str
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    capacity: Optional[int] = None


class HubCreate(HubBase):
    """Hub creation schema"""
    pass
    
    class Config:
        json_schema_extra = {
            "example": {
                "hub_name": "Chennai Central Hub",
                "city": "Chennai",
                "address": "123 Industrial Area, Chennai",
                "contact_phone": "+91-44-12345678",
                "contact_email": "chennai.hub@logistics.com",
                "capacity": 1000
            }
        }


class HubUpdate(BaseModel):
    """Hub update schema"""
    hub_name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None


class HubResponse(HubBase):
    """Hub response schema"""
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class HubListResponse(BaseModel):
    """Hub list response"""
    hubs: List[HubResponse]
    total: int
    page: int
    page_size: int


class AdminReportResponse(BaseModel):
    """Admin report response"""
    total_shipments_today: int
    delivered: int
    in_transit: int
    out_for_delivery: int
    created: int
    cancelled: int
    total_users: int
    total_customers: int
    total_agents: int
    total_hubs: int
