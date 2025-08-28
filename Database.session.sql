CREATE TABLE IF NOT EXISTS referral_triage_results (
    patient_id SERIAL PRIMARY KEY,
    patient_name TEXT NOT NULL,
    dob DATE NOT NULL,
    nhs_number TEXT NOT NULL,
    hospital_id TEXT NOT NULL,
    fake_name TEXT NOT NULL,
    source_file TEXT NOT NULL,
    result TEXT NOT NULL,
    rationale TEXT NOT NULL
);



