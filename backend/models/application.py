from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from database import Base

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicant_profiles.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    status = Column(String, default="draft")
    result = Column(String, nullable=True)
    is_selected = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
