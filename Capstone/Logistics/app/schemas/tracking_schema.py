"""
Tracking schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class TrackingUpdateCreate(BaseModel):
    """Tracking update creation schema"""
    location: str
    status: str
    description: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": "Salem Hub",
                "status": "in_transit",
                "description": "Package scanned at Salem hub"
            }
        }


class TrackingUpdateResponse(BaseModel):
    """Tracking update response schema"""
    id: UUID
    shipment_id: UUID
    location: str
    status: str
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class TrackingHistoryResponse(BaseModel):
    """Complete tracking history response"""
    tracking_number: str
    updates: List[TrackingUpdateResponse]
    total_updates: int
