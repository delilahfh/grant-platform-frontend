
from sqlalchemy import Column, Integer, String, Date, Boolean
from database import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    financial_deadline = Column(Date)
    narrative_deadline = Column(Date)
    inquiry_deadline = Column(Date)
    reporting_months = Column(Integer)
    active = Column(Boolean, default=True)
