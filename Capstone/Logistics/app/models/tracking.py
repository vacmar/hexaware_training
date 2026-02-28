"""
Tracking update model
"""
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel
from .types import GUID


class TrackingUpdate(BaseModel):
    """Tracking update model for shipment history"""
    __tablename__ = "tracking_updates"
    
    shipment_id = Column(GUID(), ForeignKey("shipments.id"), nullable=False)
    shipment = relationship("Shipment", back_populates="tracking_updates")
    
    location = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<TrackingUpdate(id={self.id}, shipment_id={self.shipment_id}, status={self.status})>"
