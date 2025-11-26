from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ApplicantProfile(Base):
    __tablename__ = "applicant_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    applicant_type = Column(String, nullable=False)
    locations = Column(String)
    address = Column(String)
    entity_name = Column(String)
    primary_name = Column(String)
    primary_email = Column(String)
    primary_dob = Column(String)
    primary_gender = Column(String)
    primary_gender_other = Column(String, nullable=True)
    secondary_name = Column(String, nullable=True)
    secondary_email = Column(String, nullable=True)
    secondary_dob = Column(String, nullable=True)
    secondary_gender = Column(String, nullable=True)
    secondary_gender_other = Column(String, nullable=True)
    user = relationship("User", backref="applicant_profile")
