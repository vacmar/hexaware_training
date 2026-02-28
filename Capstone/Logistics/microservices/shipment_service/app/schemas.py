"""
Shipment schemas
"""
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


class ShipmentStatus(str, Enum):
    """Shipment status enumeration"""
    CREATED = "created"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    AT_HUB = "at_hub"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"


class ShipmentCreate(BaseModel):
    """Schema for creating a new shipment"""
    source_address: str
    destination_address: str
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "source_address": "123 Sender St, City A",
                "destination_address": "456 Receiver Ave, City B",
                "weight": 2.5,
                "dimensions": "10x20x15",
                "description": "Electronics - Handle with care"
            }
        }


class ShipmentUpdate(BaseModel):
    """Schema for updating a shipment"""
    source_address: Optional[str] = None
    destination_address: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    description: Optional[str] = None


class ShipmentStatusUpdate(BaseModel):
    """Schema for updating shipment status"""
    status: ShipmentStatus
    location: str
    description: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "in_transit",
                "location": "Distribution Center A",
                "description": "Package in transit to destination city"
            }
        }


class ShipmentResponse(BaseModel):
    """Shipment response schema"""
    id: UUID
    tracking_number: str
    customer_id: UUID
    agent_id: Optional[UUID] = None
    current_hub_id: Optional[UUID] = None
    source_address: str
    destination_address: str
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    description: Optional[str] = None
    status: ShipmentStatus
    current_location: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ShipmentListResponse(BaseModel):
    """Paginated shipment list response"""
    shipments: list[ShipmentResponse]
    total: int
    skip: int
    limit: int


class AssignAgentRequest(BaseModel):
    """Schema for assigning agent to shipment"""
    agent_id: UUID
