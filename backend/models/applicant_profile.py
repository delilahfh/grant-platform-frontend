
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class ApplicantProfile(Base):
    __tablename__ = "applicant_profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    applicant_type = Column(String)
    locations = Column(String)
    address = Column(String)
    primary_name = Column(String)
    primary_email = Column(String)
    primary_dob = Column(String)
    primary_gender = Column(String)
    primary_gender_other = Column(String)
    secondary_name = Column(String)
    secondary_email = Column(String)
    secondary_dob = Column(String)
    secondary_gender = Column(String)
    secondary_gender_other = Column(String)
