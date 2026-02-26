from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class ApplicationStatus(str, enum.Enum):
    APPLIED = "applied"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", name="fk_application_user"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", name="fk_application_job"), nullable=False, index=True)
    status = Column(SQLEnum(ApplicationStatus), nullable=False, default=ApplicationStatus.APPLIED)
    
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
