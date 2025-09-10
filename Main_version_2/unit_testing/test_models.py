import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Main_version_2.models import Base, ReferralTriageResult

@pytest.fixture
def session():
    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_model_can_insert_and_query(session):
    # Create a sample record with correct date type
    record = ReferralTriageResult(
        patient_name="John Doe",
        source_file="referral1.pdf",
        dob=date(1980, 1, 1),  # Correct type for Date column
        nhs_number="1234567890",
        hospital_id="HOSP001",
        fake_name="Patient A",
        result="Priority 2",
        rationale="Risk of deterioration"
    )
    session.add(record)
    session.commit()

    # Query the record back
    retrieved = session.query(ReferralTriageResult).first()
    assert retrieved.patient_name == "John Doe"
    assert retrieved.result == "Priority 2"
    assert retrieved.rationale == "Risk of deterioration"
    assert retrieved.dob == date(1980, 1, 1)
