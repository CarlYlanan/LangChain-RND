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
        # This regex now stops capturing before the next field label like "Date of birth" or "Gender"
        "Patient Name": r"Patient [Nn]ame:?\s*(.*?)(?=\s\s|Date of birth)",
        "Date of Birth": r"Date of [Bb]irth:?\s*(\d{2}/\d{2}/\d{4})",
        "Gender": r"Gender:?\s*(\w+)",
        "NHS number": r"(?:NHS|NHI) [Nn]umber:?\s*[^a-zA-Z0-9]*\s*([a-zA-Z0-9]+)",
        "Email": r"(?:Patient(?:'s)?\s*|Contact\s*)?[Ee]mail(?: [Aa]ddress)?:?\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
        "Hospital ID": r"Hospital ID:?\s*([a-zA-Z0-9-_]+)",
        "GP practice identifier": r"GP practice identifier:?\s*([a-zA-Z0-9-_]+)",
        "Phone Number": r"(?:Patient\s*)?(?:[Tt]el(?:ephone)?|[Pp]hone|[Mm]obile|[Cc]ell|[Cc]ontact)\s*(?:[Nn]umber)?:?\s*(\+?[\d\s()\n-]{8,})",
        "Pregnancy": r"Pregnancy:?\s*(Yes|No|N/A|Unknown)"
    }
    patient_data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, processed_text)
        # We now use match.group(1) because the new regex has one capturing group
        patient_data[field] = match.group(1).strip() if match else None
    return patient_data


def add_data_to_db(extracted_data: dict, source_file: str):
    """
    Takes a dictionary of extracted data, checks if a patient with the same
    NHS number already exists, and if not, dynamically builds an INSERT
    statement to add the new patient to the database.
    """
    # 1. Connect to the Database
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not set in environment. Please check your .env file.")
    engine = create_engine(DATABASE_URL)

    # 2. Get the NHS number to check for uniqueness
    #nhs_number_to_check = extracted_data.get("NHS number")

    # If there's no NHS number, we can't perform the uniqueness check.
    # We will skip this record.
    #if not nhs_number_to_check:
    #    print(f"Skipping record from '{source_file}' due to missing NHS number.")
    #    return

    try:
        with engine.connect() as connection:
            # 3. Check if a patient with this NHS number already exists
            sql_check_query = text("""
                SELECT COUNT(*) FROM referral_triage_results WHERE source_file = :source_file
            """)
            result = connection.execute(sql_check_query, {"source_file": source_file}).scalar()

            if result > 0:
                #print("\n--- Database Check ---")
                print(f"Patient with NHS number '{source_file}' already exists. Skipping insertion for '{source_file}'.")
                return

            # 4. If the patient does not exist, prepare the data for insertion
            dob_str = extracted_data.get("Date of Birth")
            data_to_prepare = {
                "patient_name": extracted_data.get("Patient Name"),
                "source_file": source_file, 
                "dob": datetime.strptime(dob_str, "%d/%m/%Y").date() if dob_str else None,
                #"gender": extracted_data.get("Gender"),
                "nhs_number": extracted_data.get("NHS number"),
                #"phone_number": extracted_data.get("Phone Number"),
                #"email": extracted_data.get("Email")
                "hospital_id": extracted_data.get("Hospital ID"),
                "gp_identifier": extracted_data.get("GP practice identifier")
                
            }

            # Create a final dictionary with only the fields that have data
            final_data_to_insert = {key: value for key, value in data_to_prepare.items() if value is not None}

            if not final_data_to_insert:
                print(f"No data to insert for '{source_file}'.")
                return

            # 5. Dynamically build and execute the INSERT statement
            columns = ", ".join(final_data_to_insert.keys())
            placeholders = ", ".join(f":{key}" for key in final_data_to_insert.keys())
            
            sql_insert_query = text(f"""
                INSERT INTO referral_triage_results ({columns})
                VALUES ({placeholders})
            """)

            connection.execute(sql_insert_query, final_data_to_insert)
            connection.commit()
            #print("\n--- Database Update ---")
            print(f"Successfully inserted new patient data from '{source_file}'.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")


