
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database import Base

class CertificateOfReceipt(Base):
    __tablename__ = "certificates_of_receipt"
    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicant_profiles.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    procurement_id = Column(Integer, ForeignKey("procurements.id"))
    date = Column(Date)
    items_text = Column(String)  # newline-separated list of delivered items/services
    status = Column(String, default="DRAFT")  # DRAFT / SUBMITTED / APPROVED / REJECTED
    generated_doc_path = Column(String)
    signed_doc_path = Column(String)
