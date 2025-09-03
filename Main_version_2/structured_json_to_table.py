import re
import json
from sqlalchemy import create_engine, text
from datetime import datetime
import os
from dotenv import load_dotenv

# Load variables from .env file when this module is imported
load_dotenv()

def extract_data_from_text(processed_text: str) -> dict:
    """Helper function to extract key-value pairs from text using regex."""
    patterns = {
        # FIXED: This regex now stops capturing before the next field label like "Date of birth" or "Gender"
        "Patient Name": r"Patient [Nn]ame:?\s*(.*?)(?=\s\s|Date of birth)",
        "Date of Birth": r"Date of [Bb]irth:?\s*(\d{2}/\d{2}/\d{4})",
        "NHS number": r"NHS [Nn]umber:?\s*([a-zA-Z0-9]+)",
        "Hospital ID": r"Hospital ID:?\s*([a-zA-Z0-_]+)"
    }
    patient_data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, processed_text)
        # We now use match.group(1) because the new regex has one capturing group
        patient_data[field] = match.group(1).strip() if match else None
    return patient_data


def add_data_to_db(extracted_data: dict, source_filename: str):
    """
    Takes a dictionary of extracted data and dynamically builds an INSERT statement
    to add it to the database.
    """
    #print("--- Extracted Information ---")
    #print(json.dumps(extracted_data, indent=2))

    # 1. Connect to the Database
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not set in environment. Please check your .env file.")
    engine = create_engine(DATABASE_URL)

    # 2. Prepare the initial data dictionary, mapping to column names
    dob_str = extracted_data.get("Date of Birth")
    data_to_prepare = {
        "patient_name": extracted_data.get("Patient Name"),
        "dob": datetime.strptime(dob_str, "%d/%m/%Y").date() if dob_str else None,
        "nhs_number": extracted_data.get("NHS number"),
        "hospital_id": extracted_data.get("Hospital ID"),
        "source_file": source_filename
    }

    # 3. Create a final dictionary with only the fields that have data
    final_data_to_insert = {key: value for key, value in data_to_prepare.items() if value is not None}

    if not final_data_to_insert:
        print("No data extracted. Nothing to insert.")
        return

    # 4. Dynamically build the INSERT statement
    columns = ", ".join(final_data_to_insert.keys())
    placeholders = ", ".join(f":{key}" for key in final_data_to_insert.keys())
    
    sql_insert_query = text(f"""
        INSERT INTO referral_triage_results ({columns})
        VALUES ({placeholders})
    """)

    # 5. Execute the dynamic query
    try:
        with engine.connect() as connection:
            connection.execute(sql_insert_query, final_data_to_insert)
            connection.commit()
        #print("\n--- Database Update ---")
        #print(f"Successfully inserted data for {source_filename}.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

