

CREATE TABLE Med_results (
    id SERIAL PRIMARY KEY,
    patient_name VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    date_of_appointment TIMESTAMP,
    nhs_number VARCHAR(20) UNIQUE NOT NULL,
    hospital_id VARCHAR(50),
    address TEXT,
    email VARCHAR(255),
    medical_staff VARCHAR(255),
    symptoms TEXT,
    diagnosis TEXT,
    treatment_plan TEXT,
    urgency_value VARCHAR(50) DEFAULT 'Medium',
    record_status VARCHAR(50) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_document VARCHAR(500)
);
