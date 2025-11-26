
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Procurement(Base):
    __tablename__ = "procurements"
    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicant_profiles.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    budget_line_id = Column(Integer)
    code = Column(String)
    type = Column(String)  # consultancy/service/product/works
    description = Column(String)

class SupplierQuote(Base):
    __tablename__ = "supplier_quotes"
    id = Column(Integer, primary_key=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"))
    supplier_name = Column(String)
    price = Column(Integer)
    file_path = Column(String)
