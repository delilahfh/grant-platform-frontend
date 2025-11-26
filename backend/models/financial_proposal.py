
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime
from database import Base

class FinancialProposal(Base):
    __tablename__ = "financial_proposals"
    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicant_profiles.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class FinancialProposalVersion(Base):
    __tablename__ = "financial_proposal_versions"
    id = Column(Integer, primary_key=True)
    proposal_id = Column(Integer, ForeignKey("financial_proposals.id"))
    version_number = Column(Integer)
    is_original = Column(Boolean, default=False)
    status = Column(String, default="DRAFT")
    deadline_locked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class BudgetHeading(Base):
    __tablename__ = "budget_headings"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    order = Column(Integer)
    title = Column(String)

class BudgetLine(Base):
    __tablename__ = "budget_lines"
    id = Column(Integer, primary_key=True)
    version_id = Column(Integer, ForeignKey("financial_proposal_versions.id"))
    heading_id = Column(Integer, ForeignKey("budget_headings.id"))
    line_number = Column(String)
    name = Column(String)
    unit = Column(Integer)
    unit_cost = Column(Integer)
    cofinancing = Column(Integer)
