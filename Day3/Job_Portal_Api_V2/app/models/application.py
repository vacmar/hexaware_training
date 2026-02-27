#application.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.base import Base
from sqlalchemy.orm import relationship

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    status = Column(String) #applied / shortlisted / rejected

    job = relationship("Job", back_populates="applications")