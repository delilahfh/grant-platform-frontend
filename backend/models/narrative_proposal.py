
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime
from database import Base

class NarrativeProposal(Base):
    __tablename__ = "narrative_proposals"
    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicant_profiles.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class NarrativeProposalVersion(Base):
    __tablename__ = "narrative_proposal_versions"
    id = Column(Integer, primary_key=True)
    proposal_id = Column(Integer, ForeignKey("narrative_proposals.id"))
    version_number = Column(Integer)
    status = Column(String, default="DRAFT")
    deadline_locked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class NarrativeSection(Base):
    __tablename__ = "narrative_sections"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    order = Column(Integer)
    title = Column(String)

class NarrativeEntry(Base):
    __tablename__ = "narrative_entries"
    id = Column(Integer, primary_key=True)
    version_id = Column(Integer, ForeignKey("narrative_proposal_versions.id"))
    section_id = Column(Integer, ForeignKey("narrative_sections.id"))
    content = Column(String)
