
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class EvaluationReport(Base):
    __tablename__ = "evaluation_reports"
    id = Column(Integer, primary_key=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"))
    eligibility = Column(String)
    quality = Column(String)
    preferential = Column(String)
    risks = Column(String)
    selected_supplier = Column(String)

class EvaluationScore(Base):
    __tablename__ = "evaluation_scores"
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey("evaluation_reports.id"))
    supplier_name = Column(String)
    score = Column(Integer)
