
from sqlalchemy import Column, Integer, String
from database import Base

class ContractField(Base):
    __tablename__ = "contract_fields"
    id = Column(Integer, primary_key=True)
    field_name = Column(String)
    label = Column(String)
    required = Column(String)  # yes/no
    visible_for = Column(String)  # individual / organization / both
