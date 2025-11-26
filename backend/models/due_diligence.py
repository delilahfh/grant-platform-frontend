
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class DueDiligenceType(Base):
    __tablename__ = "due_diligence_types"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String)

class DueDiligenceFile(Base):
    __tablename__ = "due_diligence_files"
    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicant_profiles.id"))
    type_id = Column(Integer, ForeignKey("due_diligence_types.id"))
    file_path = Column(String)
