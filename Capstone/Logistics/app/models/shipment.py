"""
Shipment model
"""
import enum
import uuid
from sqlalchemy import Column, String, Text, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import BaseModel
from .types import GUID


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


def generate_tracking_number():
    """Generate a unique tracking number"""
    return f"TRK{uuid.uuid4().hex[:10].upper()}"


class Shipment(BaseModel):
    """Shipment model"""
    __tablename__ = "shipments"
    
    tracking_number = Column(String(20), unique=True, index=True, default=generate_tracking_number)
    
    # Customer relationship
    customer_id = Column(GUID(), ForeignKey("users.id"), nullable=False)
    customer = relationship("User", foreign_keys=[customer_id], backref="shipments")
    
    # Assigned agent (delivery agent)
    agent_id = Column(GUID(), ForeignKey("users.id"), nullable=True)
    agent = relationship("User", foreign_keys=[agent_id], backref="assigned_shipments")
    
    # Current hub
    current_hub_id = Column(GUID(), ForeignKey("hubs.id"), nullable=True)
    current_hub = relationship("Hub", backref="current_shipments")
    
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
    
    # Tracking updates relationship
    tracking_updates = relationship("TrackingUpdate", back_populates="shipment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Shipment(id={self.id}, tracking_number={self.tracking_number}, status={self.status})>"
