
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class NarrativeReport(Base):
    __tablename__ = "narrative_reports"
    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicant_profiles.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    version_number = Column(Integer)
    period_start = Column(String)
    period_end = Column(String)
    status = Column(String, default="DRAFT")

class NarrativeReportSection(Base):
    __tablename__ = "narrative_report_sections"
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey("narrative_reports.id"))
    title = Column(String)
    kpi = Column(String)
    activity = Column(String)
    status = Column(String)
    date_of_completion = Column(String)
    related_budget_line = Column(String)
    description = Column(String)
