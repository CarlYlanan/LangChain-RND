from sqlalchemy import create_engine, Column, String, Date, Text, TIMESTAMP, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel, Field, EmailStr, ValidationError
from typing import List, Optional
from datetime import date, datetime

Base = declarative_base()

# SQLAlchemy ORM table definition
class MedResult(Base):
    __tablename__ = 'med_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_name = Column(String(255), nullable=False)
    date_of_birth = Column(Date)
    date_of_appointment = Column(TIMESTAMP)
    nhs_number = Column(String(20), unique=True, nullable=False)
    hospital_id = Column(String(50))
    address = Column(Text)
    email = Column(String(255))
    medical_staff = Column(String(255))
    symptoms = Column(Text)
    diagnosis = Column(Text)
    treatment_plan = Column(Text)
    urgency_value = Column(String(50), default='Medium')
    record_status = Column(String(50), default='Active')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    source_document = Column(String(500))

# Pydantic model for validation
class MedResultData(BaseModel):
    patient_name: str
    date_of_birth: Optional[date]
    date_of_appointment: Optional[datetime]
    nhs_number: str
    hospital_id: Optional[str]
    address: Optional[str]
    email: Optional[str]
    medical_staff: Optional[str]
    symptoms: Optional[str]
    diagnosis: Optional[str]
    treatment_plan: Optional[str]
    urgency_value: Optional[str] = "Medium"
    record_status: Optional[str] = "Active"
    source_document: Optional[str]

def insert_validated_med_results(patients_data: List[dict], db_name='your_db', user='your_user', password='your_password', host='localhost', port='5432'):
    """
    Validates and inserts a batch of Med_results records into PostgreSQL.
    """
    try:
        engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        valid_records = []
        for entry in patients_data:
            try:
                validated = MedResultData(**entry)
                record = MedResult(
                    patient_name=validated.patient_name,
                    date_of_birth=validated.date_of_birth,
                    date_of_appointment=validated.date_of_appointment,
                    nhs_number=validated.nhs_number,
                    hospital_id=validated.hospital_id,
                    address=validated.address,
                    email=validated.email,
                    medical_staff=validated.medical_staff,
                    symptoms=validated.symptoms,
                    diagnosis=validated.diagnosis,
                    treatment_plan=validated.treatment_plan,
                    urgency_value=validated.urgency_value,
                    record_status=validated.record_status,
                    source_document=validated.source_document
                )
                valid_records.append(record)
            except ValidationError as ve:
                print(f"Validation error for record: {entry.get('nhs_number', 'N/A')} — {ve}")

        if valid_records:
            session.bulk_save_objects(valid_records)
            session.commit()
            print(f"{len(valid_records)} records inserted successfully.")
        else:
            print("No valid records to insert.")

        session.close()

    except SQLAlchemyError as e:
        print("Database error:", e)
