"""
Hub schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


class HubCreate(BaseModel):
    """Schema for creating a new hub"""
    hub_name: str
    city: str
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    capacity: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "hub_name": "Central Distribution Hub",
                "city": "New York",
                "address": "123 Main St, New York, NY 10001",
                "contact_phone": "+1234567890",
                "contact_email": "hub@logistics.com",
                "capacity": 1000
            }
        }


class HubUpdate(BaseModel):
    """Schema for updating a hub"""
    hub_name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None


class HubResponse(BaseModel):
    """Hub response schema"""
    id: UUID
    hub_name: str
    city: str
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    capacity: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class HubListResponse(BaseModel):
    """Paginated hub list response"""
    hubs: list[HubResponse]
    total: int
    skip: int
    limit: int
