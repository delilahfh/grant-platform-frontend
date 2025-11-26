
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class FinancialReport(Base):
    __tablename__ = "financial_reports"
    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicant_profiles.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    version_number = Column(Integer)
    status = Column(String, default="DRAFT")

class FinancialReportExpenditure(Base):
    __tablename__ = "financial_report_expenditures"
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey("financial_reports.id"))
    procurement_code = Column(String)
    date = Column(String)
    budget_line = Column(String)
    cost = Column(Integer)
    currency = Column(String)
    notes = Column(String)
