from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class ReferralTriageResult(Base):
    __tablename__ = 'referral_triage_results'

    patient_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    nhs_number = Column(String, nullable=False)
    hospital_id = Column(String, nullable=False)
    fake_name = Column(String, nullable=False)
    source_file = Column(String, nullable=False)
    result = Column(String, nullable=False)
    rationale = Column(String, nullable=False)