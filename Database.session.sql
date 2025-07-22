--DROP TABLE IF EXISTS Med_results;
--DROP TABLE IF EXISTS Recent_Updates;

-- Main Database (For RAG)
CREATE TABLE Med_results (
    patient_id SERIAL PRIMARY KEY,

    -- Patient demographics
    patient_name VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(50),
    nhs_number VARCHAR(20) UNIQUE NOT NULL,
    hospital_id VARCHAR(50),
    patient_address TEXT,
    patient_email VARCHAR(255),
    patient_phone_number VARCHAR(50),

    -- Appointment details
    date_of_appointment TIMESTAMP,
    contact_type VARCHAR(100),
    consultation_method VARCHAR(100),
    seen_by VARCHAR(255),
    outcome TEXT,

    -- GP practice details
    gp_name VARCHAR(255),
    gp_practice_id VARCHAR(50),
    gp_address TEXT,
    gp_contact_number VARCHAR(50),

    -- Clinical summary
    diagnosis TEXT,
    issues TEXT,
    clinical_history TEXT,
    weight_kg DECIMAL(5,2),
    height_cm DECIMAL(5,2),
    bmi DECIMAL(5,2),
    estimated_energy_kcal INT,
    estimated_protein_g INT,
    estimated_fluid_ml INT,
    bowel_function TEXT,
    pressure_area_status TEXT,
    allergies TEXT,
    feeding_regimen TEXT,

    -- Medication/device details
    medication_name VARCHAR(255),
    medication_form VARCHAR(100),
    administration_route VARCHAR(100),
    administration_site VARCHAR(100),
    administration_method VARCHAR(100),
    dose_amount VARCHAR(100),
    dose_schedule TEXT,
    additional_instructions TEXT,
    medication_status VARCHAR(100),
    medication_change_reason TEXT,
    medication_change_date DATE,
    medication_change_description TEXT,
    pharmacy_contact TEXT,
    medication_comment TEXT,

    -- Actions and recommendations
    actions_for_staff TEXT,
    actions_for_patient TEXT,
    advice_given TEXT,

    -- Record metadata
    completed_by VARCHAR(255),
    record_completion_date TIMESTAMP,
    record_status VARCHAR(50) DEFAULT 'Active',
    urgency_value VARCHAR(50) DEFAULT 'Medium',
    source_document VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Secondary Table for Recent Updates
CREATE TABLE Recent_Updates (
    patient_id SERIAL PRIMARY KEY,

    -- Patient Info
    patient_name VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(50),
    nhs_number VARCHAR(20) UNIQUE NOT NULL,
    hospital_id VARCHAR(50),
    patient_address TEXT,
    patient_email VARCHAR(255),
    patient_phone_number VARCHAR(50),

    -- Appointment Details
    date_of_appointment TIMESTAMP,
    contact_type VARCHAR(100),
    consultation_method VARCHAR(100),
    seen_by VARCHAR(255),
    outcome TEXT,

    -- GP Info
    gp_name VARCHAR(255),
    gp_practice_id VARCHAR(50),
    gp_address TEXT,
    gp_contact_number VARCHAR(50),

    -- Clinical Summary
    diagnosis TEXT,
    issues TEXT,
    clinical_history TEXT,
    weight_kg DECIMAL(5,2),
    height_cm DECIMAL(5,2),
    bmi DECIMAL(5,2),
    estimated_energy_kcal INT,
    estimated_protein_g INT,
    estimated_fluid_ml INT,
    bowel_function TEXT,
    pressure_area_status TEXT,
    allergies TEXT,
    feeding_regimen TEXT,

    -- Medication and Device Changes
    medication_name VARCHAR(255),
    medication_form VARCHAR(100),
    administration_route VARCHAR(100),
    administration_site VARCHAR(100),
    administration_method VARCHAR(100),
    dose_amount VARCHAR(100),
    dose_schedule TEXT,
    additional_instructions TEXT,
    medication_status VARCHAR(100),
    medication_change_reason TEXT,
    medication_change_date DATE,
    medication_change_description TEXT,
    pharmacy_contact TEXT,
    medication_comment TEXT,

    -- Actions and Notes
    actions_for_staff TEXT,
    actions_for_patient TEXT,
    advice_given TEXT,

    -- Metadata
    completed_by VARCHAR(255),
    record_completion_date TIMESTAMP,
    record_status VARCHAR(50) DEFAULT 'Active',
    urgency_value VARCHAR(50) DEFAULT 'Medium',
    source_document VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
