
from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicant_profiles.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    active_version_id = Column(Integer, ForeignKey("contract_versions.id"), nullable=True)
