
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database import Base

class RequestInstalment(Base):
    __tablename__ = "request_instalments"
    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicant_profiles.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    instalment_number = Column(Integer)
    request_number = Column(String)
    amount_number = Column(Integer)
    amount_words = Column(String)
    account_name = Column(String)
    account_number = Column(String)
    iban = Column(String)
    swift = Column(String)
    bank_name = Column(String)
    status = Column(String, default="DRAFT")
    signed_doc_path = Column(String)
    date = Column(Date)
