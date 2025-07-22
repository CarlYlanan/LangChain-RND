from sqlalchemy import (
    Column, Integer, String, Date, Text, TIMESTAMP, DECIMAL, func
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MedResult(Base):
    __tablename__ = 'med_results'

    patient_id = Column(Integer, primary_key=True, autoincrement=True)

    # Patient Info
    patient_name = Column(String(255), nullable=False)
    date_of_birth = Column(Date)
    gender = Column(String(50))
    nhs_number = Column(String(20), unique=True, nullable=False)
    hospital_id = Column(String(50))
    patient_address = Column(Text)
    patient_email = Column(String(255))
    patient_phone_number = Column(String(50))

    # Appointment Details
    date_of_appointment = Column(TIMESTAMP)
    contact_type = Column(String(100))
    consultation_method = Column(String(100))
    seen_by = Column(String(255))
    outcome = Column(Text)

    # GP Info
    gp_name = Column(String(255))
    gp_practice_id = Column(String(50))
    gp_address = Column(Text)
    gp_contact_number = Column(String(50))

    # Clinical Summary
    diagnosis = Column(Text)
    issues = Column(Text)
    clinical_history = Column(Text)
    weight_kg = Column(DECIMAL(5, 2))
    height_cm = Column(DECIMAL(5, 2))
    bmi = Column(DECIMAL(5, 2))
    estimated_energy_kcal = Column(Integer)
    estimated_protein_g = Column(Integer)
    estimated_fluid_ml = Column(Integer)
    bowel_function = Column(Text)
    pressure_area_status = Column(Text)
    allergies = Column(Text)
    feeding_regimen = Column(Text)

    # Medication and Device Changes
    medication_name = Column(String(255))
    medication_form = Column(String(100))
    administration_route = Column(String(100))
    administration_site = Column(String(100))
    administration_method = Column(String(100))
    dose_amount = Column(String(100))
    dose_schedule = Column(Text)
    additional_instructions = Column(Text)
    medication_status = Column(String(100))
    medication_change_reason = Column(Text)
    medication_change_date = Column(Date)
    medication_change_description = Column(Text)
    pharmacy_contact = Column(Text)
    medication_comment = Column(Text)

    # Actions and Notes
    actions_for_staff = Column(Text)
    actions_for_patient = Column(Text)
    advice_given = Column(Text)

    # Metadata
    completed_by = Column(String(255))
    record_completion_date = Column(TIMESTAMP)
    record_status = Column(String(50), default='Active')
    urgency_value = Column(String(50), default='Medium')
    source_document = Column(String(500))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class RecentUpdate(Base):
    __tablename__ = 'recent_updates'

    patient_id = Column(Integer, primary_key=True, autoincrement=True)

    # Patient Info
    patient_name = Column(String(255), nullable=False)
    date_of_birth = Column(Date)
    gender = Column(String(50))
    nhs_number = Column(String(20), unique=True, nullable=False)
    hospital_id = Column(String(50))
    patient_address = Column(Text)
    patient_email = Column(String(255))
    patient_phone_number = Column(String(50))

    # Appointment Details
    date_of_appointment = Column(TIMESTAMP)
    contact_type = Column(String(100))
    consultation_method = Column(String(100))
    seen_by = Column(String(255))
    outcome = Column(Text)

    # GP Info
    gp_name = Column(String(255))
    gp_practice_id = Column(String(50))
    gp_address = Column(Text)
    gp_contact_number = Column(String(50))

    # Clinical Summary
    diagnosis = Column(Text)
    issues = Column(Text)
    clinical_history = Column(Text)
    weight_kg = Column(DECIMAL(5, 2))
    height_cm = Column(DECIMAL(5, 2))
    bmi = Column(DECIMAL(5, 2))
    estimated_energy_kcal = Column(Integer)
    estimated_protein_g = Column(Integer)
    estimated_fluid_ml = Column(Integer)
    bowel_function = Column(Text)
    pressure_area_status = Column(Text)
    allergies = Column(Text)
    feeding_regimen = Column(Text)

    # Medication and Device Changes
    medication_name = Column(String(255))
    medication_form = Column(String(100))
    administration_route = Column(String(100))
    administration_site = Column(String(100))
    administration_method = Column(String(100))
    dose_amount = Column(String(100))
    dose_schedule = Column(Text)
    additional_instructions = Column(Text)
    medication_status = Column(String(100))
    medication_change_reason = Column(Text)
    medication_change_date = Column(Date)
    medication_change_description = Column(Text)
    pharmacy_contact = Column(Text)
    medication_comment = Column(Text)

    # Actions and Notes
    actions_for_staff = Column(Text)
    actions_for_patient = Column(Text)
    advice_given = Column(Text)

    # Metadata
    completed_by = Column(String(255))
    record_completion_date = Column(TIMESTAMP)
    record_status = Column(String(50), default='Active')
    urgency_value = Column(String(50), default='Medium')
    source_document = Column(String(500))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
