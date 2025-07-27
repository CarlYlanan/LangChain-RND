-- Drop tables if needed
-- DROP TABLE IF EXISTS patient_results;
-- DROP TABLE IF EXISTS notes_to_triage;
-- DROP TABLE IF EXISTS rules;
-- DROP TABLE IF EXISTS patients;

-- Patients (information extracted from structured data)
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    dob DATE,
    gender VARCHAR(50),
    nhs_number VARCHAR(20) UNIQUE NOT NULL,
    phone_number VARCHAR(50),
    email VARCHAR(255),
    pregnancy BOOLEAN,
);

-- Notes to Triage (information extracted from all types of data)
CREATE TABLE notes_to_triage (
    note_id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, completed, error
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rules for the grading algorithm
CREATE TABLE rules (
    rule_id SERIAL PRIMARY KEY,
    priority VARCHAR(50),
    target_timeframe VARCHAR(50),
    referral_category VARCHAR(100),
    symptoms TEXT,
    trigger_terms TEXT,
    clinical_context TEXT,
    age_min INTEGER
);

-- Patient Results (this is information once triaging is completed)
CREATE TABLE patient_results (
    result_id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id) ON DELETE CASCADE,
    note_id INTEGER REFERENCES notes_to_triage(note_id) ON DELETE CASCADE,
    rule_id INTEGER REFERENCES rules(rule_id),
    matched_trigger_terms TEXT,
    negation_detected BOOLEAN,
    confidence_score DECIMAL(3,2),
    triaged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
