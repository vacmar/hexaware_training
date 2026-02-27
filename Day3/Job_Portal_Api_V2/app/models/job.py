#job.py

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.base import Base
from sqlalchemy.orm import relationship

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    salary = Column(Integer)
    company_id = Column(Integer, ForeignKey("companies.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    
    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")