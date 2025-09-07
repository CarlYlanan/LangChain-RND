from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class ReferralTriageResult(Base):
    __tablename__ = 'referral_triage_results'

    patient_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_name = Column(String, nullable=False)
    source_file = Column(String, nullable=False)
    dob = Column(Date)
    nhs_number = Column(String)
    hospital_id = Column(String)
    fake_name = Column(String)
    result = Column(String)
    rationale = Column(String)