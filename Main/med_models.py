from sqlalchemy import (
    Column, Integer, String, Date, Text, Boolean, ForeignKey, DECIMAL, TIMESTAMP, func
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Patients info
class Patient(Base):
    __tablename__ = 'patients'

    patient_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    dob = Column(Date)
    gender = Column(String(50))
    nhs_number = Column(String(20), unique=True, nullable=False)
    phone_number = Column(String(50))
    email = Column(String(255))
    pregnancy = Column(Boolean)

    #Relationships through primary and foreign keys
    notes = relationship('NoteToTriage', back_populates='patient')
    results = relationship('PatientResult', back_populates='patient')


# Notes to triage
class NoteToTriage(Base):
    __tablename__ = 'notes_to_triage'

    note_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'))
    text = Column(Text, nullable=False)
    status = Column(String(20), default='pending')
    created_at = Column(TIMESTAMP, server_default=func.now())

    #Relationships through primary and foreign keys
    patient = relationship('Patient', back_populates='notes')
    results = relationship('PatientResult', back_populates='note')


# Rules for grading algorithm 
class Rule(Base):
    __tablename__ = 'rules'

    rule_id = Column(Integer, primary_key=True, autoincrement=True)
    priority = Column(String(50))
    target_timeframe = Column(String(50))
    referral_category = Column(String(100))
    symptoms = Column(Text)
    trigger_terms = Column(Text)
    clinical_context = Column(Text)
    age_min = Column(Integer)

    # This relationship lets you access all PatientResult info associated with a given Rule
    results = relationship('PatientResult', back_populates='rule')


# Final patient results
class PatientResult(Base):
    __tablename__ = 'patient_results'

    result_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id', ondelete='CASCADE'))
    note_id = Column(Integer, ForeignKey('notes_to_triage.note_id', ondelete='CASCADE'))
    rule_id = Column(Integer, ForeignKey('rules.rule_id'))
    matched_trigger_terms = Column(Text)
    negation_detected = Column(Boolean)
    confidence_score = Column(DECIMAL(3, 2))
    triaged_at = Column(TIMESTAMP, server_default=func.now())

    #Relationships through primary and foreign keys
    patient = relationship('Patient', back_populates='results')
    note = relationship('NoteToTriage', back_populates='results')
    rule = relationship('Rule', back_populates='results')

