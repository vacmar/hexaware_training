"""
Tracking schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class TrackingUpdateCreate(BaseModel):
    """Schema for creating a tracking update"""
    location: str
    status: str
    description: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": "Distribution Hub A",
                "status": "in_transit",
                "description": "Package arrived at distribution center"
            }
        }


class TrackingUpdateResponse(BaseModel):
    """Tracking update response schema"""
    id: UUID
    shipment_id: UUID
    location: str
    status: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TrackingHistoryResponse(BaseModel):
    """Complete tracking history response"""
    shipment_id: UUID
    tracking_number: Optional[str] = None
    current_status: Optional[str] = None
    current_location: Optional[str] = None
    updates: List[TrackingUpdateResponse]


class ShipmentInfo(BaseModel):
    """Basic shipment info from shipment service"""
    id: UUID
    tracking_number: str
    status: str
    current_location: Optional[str] = None
