
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database import Base

class PaymentRecord(Base):
    __tablename__ = "payment_records"
    id = Column(Integer, primary_key=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"))
    amount = Column(Integer)
    currency = Column(String)
    date = Column(Date)
    invoice_path = Column(String)
    receipt_path = Column(String)
    verification_path = Column(String)
