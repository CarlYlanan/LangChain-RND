CREATE TABLE IF NOT EXISTS referral_triage_results (
    patient_id SERIAL PRIMARY KEY,
    patient_name TEXT NOT NULL,
    source_file TEXT NOT NULL,
    dob DATE,
    nhs_number TEXT,
    hospital_id TEXT,
    gp_identifier TEXT, 
    result TEXT DEFAULT 'Pending Triage',
    rationale TEXT DEFAULT ''
);