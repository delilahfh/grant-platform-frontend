
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class ContractType(Base):
    __tablename__ = "contract_types"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String)
    template_path = Column(String)
    rules_json = Column(String)  # json string: visibility rules
