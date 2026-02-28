"""
Shipment schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from ..models.shipment import ShipmentStatus


class ShipmentBase(BaseModel):
    """Base shipment schema"""
    source_address: str
    destination_address: str
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    description: Optional[str] = None


class ShipmentCreate(ShipmentBase):
    """Shipment creation schema"""
    pass
    
    class Config:
        json_schema_extra = {
            "example": {
                "source_address": "Chennai, Tamil Nadu",
                "destination_address": "Bangalore, Karnataka",
                "weight": 2.5,
                "dimensions": "10x20x30",
                "description": "Electronics package"
            }
        }


class ShipmentUpdate(BaseModel):
    """Shipment update schema"""
    source_address: Optional[str] = None
    destination_address: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    description: Optional[str] = None


class ShipmentStatusUpdate(BaseModel):
    """Shipment status update schema (for agents)"""
    status: ShipmentStatus
    location: str
    description: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "in_transit",
                "location": "Salem Hub",
                "description": "Package arrived at Salem hub"
            }
        }


class ShipmentAssignAgent(BaseModel):
    """Assign agent to shipment schema"""
    agent_id: UUID


class TrackingUpdateResponse(BaseModel):
    """Tracking update response schema"""
    id: UUID
    location: str
    status: str
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ShipmentResponse(ShipmentBase):
    """Shipment response schema"""
    id: UUID
    tracking_number: str
    customer_id: UUID
    agent_id: Optional[UUID]
    current_hub_id: Optional[UUID]
    status: ShipmentStatus
    current_location: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ShipmentDetailResponse(ShipmentResponse):
    """Detailed shipment response with tracking history"""
    tracking_updates: List[TrackingUpdateResponse] = []


class ShipmentTrackResponse(BaseModel):
    """Simplified tracking response"""
    tracking_number: str
    status: ShipmentStatus
    current_location: Optional[str]
    source_address: str
    destination_address: str
    tracking_updates: List[TrackingUpdateResponse] = []
    
    class Config:
        from_attributes = True


class ShipmentListResponse(BaseModel):
    """Shipment list response"""
    shipments: List[ShipmentResponse]
    total: int
    page: int
    page_size: int
