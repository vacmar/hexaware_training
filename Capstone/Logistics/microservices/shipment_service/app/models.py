"""
Shipment model
"""
import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Enum, Float, DateTime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from shared.database import Base
from shared.types import GUID


def generate_tracking_number():
    """Generate a unique tracking number"""
    return f"TRK{uuid.uuid4().hex[:10].upper()}"


class ShipmentStatus(str, enum.Enum):
    """Shipment status enumeration"""
    CREATED = "created"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    AT_HUB = "at_hub"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"


class Shipment(Base):
    """Shipment model"""
    __tablename__ = "shipments"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    tracking_number = Column(String(20), unique=True, index=True, default=generate_tracking_number)
    
    # Customer ID (reference to user in auth service)
    customer_id = Column(GUID(), nullable=False)
    
    # Assigned agent ID (reference to user in auth service)
    agent_id = Column(GUID(), nullable=True)
    
    # Current hub ID (reference to hub in hub service)
    current_hub_id = Column(GUID(), nullable=True)
    
    # Addresses
    source_address = Column(Text, nullable=False)
    destination_address = Column(Text, nullable=False)
    
    # Package details
    weight = Column(Float, nullable=True)
    dimensions = Column(String(100), nullable=True)  # e.g., "10x20x30"
    description = Column(Text, nullable=True)
    
    # Status
    status = Column(Enum(ShipmentStatus), default=ShipmentStatus.CREATED, nullable=False)
    current_location = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<Shipment(id={self.id}, tracking_number={self.tracking_number}, status={self.status})>"
