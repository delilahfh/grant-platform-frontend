
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database import Base

class ContractVersion(Base):
    __tablename__ = "contract_versions"
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    version_number = Column(Integer)
    generated_doc_path = Column(String)
    signed_doc_path = Column(String)
    status = Column(String, default="DRAFT")
    signature_date = Column(Date)
