from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from database import Base

class PaymentRequest(Base):
    __tablename__ = "payment_requests"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    instalment_number = Column(Integer)
    status = Column(String, default="submitted")
    created_at = Column(DateTime, default=datetime.utcnow)
