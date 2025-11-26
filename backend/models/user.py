
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="applicant")  # applicant/admin
    banned = Column(Boolean, default=False)
