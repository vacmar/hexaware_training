"""
Tracking update model
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from shared.database import Base
from shared.types import GUID


class TrackingUpdate(Base):
    """Tracking update model for shipment history"""
    __tablename__ = "tracking_updates"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    shipment_id = Column(GUID(), nullable=False, index=True)
    
    location = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<TrackingUpdate(id={self.id}, shipment_id={self.shipment_id}, status={self.status})>"
