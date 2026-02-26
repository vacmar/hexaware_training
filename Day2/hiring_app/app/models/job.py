from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    company_id = Column(Integer, nullable=False)
    
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
