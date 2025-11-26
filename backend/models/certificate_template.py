
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class CertificateTemplate(Base):
    __tablename__ = "certificate_templates"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)  # null = universal
    title = Column(String)
    template_path = Column(String)
