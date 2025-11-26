from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from database import Base

class FinancialReport(Base):
    __tablename__ = "financial_reports"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    period_label = Column(String)
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)

class NarrativeReport(Base):
    __tablename__ = "narrative_reports"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    period_label = Column(String)
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
