import os
from datetime import date, datetime
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, OperationalError
from langchain_openai import ChatOpenAI

# Import your models and schemas
from med_models import Base, Patient, NoteToTriage, Rule, PatientResult # Import all models
from schemas import MedicalKeywordExtraction, PatientDemographics # Import the new schema

# Load environment variables
load_dotenv(dotenv_path=".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Use OPENAI_API_KEY as per LangChain
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file.")

# --- Database Connection Configuration ---
DB_USER = os.getenv("PG_USER", "postgres")
DB_PASSWORD = os.getenv("PG_PASSWORD", "password")
DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", "5432")
DB_NAME = os.getenv("PG_DB_NAME", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- Setup SQLAlchemy Engine and Session ---
try:
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db_session = Session() # Renamed to db_session to avoid conflict with LangChain 'session'

    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    print(f"Successfully connected to PostgreSQL database '{DB_NAME}'.")
    print("Tables checked/created.")

except OperationalError as e:
    print(f"Error connecting to the database: {e}")
    print("Please ensure PostgreSQL is running and your connection details in .env are correct.")
    exit()

# --- Initialize LLM with structured output ---
llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)
structured_llm = llm.with_structured_output(MedicalKeywordExtraction, method="function_calling")

# --- Function to extract and process patient data from text ---
def extract_and_process_patient_data(input_text: str):
    print("\n--- Sending text to LLM for extraction ---")
    try:
        # Use .invoke() for single synchronous call or .stream() and collect full response
        # For simplicity, using .invoke() here which waits for full response
        extracted_data: MedicalKeywordExtraction = structured_llm.invoke(input_text)
        print("--- LLM extraction complete ---")
        # print(f"Extracted Raw Data: {extracted_data}") # For debugging

        # Extract demographics
        demographics: PatientDemographics = extracted_data.get("demographics", {})

        # --- Data Validation and Transformation ---
        # Name and NHS Number are crucial
        name = demographics.get("name")
        nhs_number = demographics.get("nhs_number")

        if not name:
            print("Warning: Patient name could not be extracted. Cannot proceed with database insertion.")
            return
        if not nhs_number:
            print("Warning: Patient NHS Number could not be extracted. Cannot proceed with database insertion.")
            return

        # Convert DOB string to date object
        dob: Optional[date] = None
        if demographics.get("dob"):
            try:
                dob = date.fromisoformat(demographics["dob"])
            except ValueError:
                print(f"Warning: Invalid DOB format '{demographics['dob']}'. Setting DOB to NULL.")

        # Convert pregnancy to boolean
        pregnancy: Optional[bool] = demographics.get("pregnancy")
        if pregnancy is not None and not isinstance(pregnancy, bool):
            # LLM might return "True" as string, try to convert
            pregnancy = str(pregnancy).lower() == 'true'

        # --- Create and Store Patient Record ---
        new_patient = Patient(
            name=name,
            dob=dob,
            gender=demographics.get("gender"),
            nhs_number=nhs_number,
            phone_number=demographics.get("phone_number"),
            email=demographics.get("email"),
            pregnancy=pregnancy
        )

        try:
            db_session.add(new_patient)
            db_session.commit()
            print(f"\nSuccessfully added Patient '{new_patient.name}' (NHS: {new_patient.nhs_number}) to the database.")
            print(f"Assigned Patient ID: {new_patient.patient_id}")

            # Optionally, you could also store the raw note or extracted keywords here
            # For instance, if you want to save the original text as a NoteToTriage
            # or the extracted diagnoses/symptoms for later use.
            # Example to save the note itself:
            new_note = NoteToTriage(
                patient_id=new_patient.patient_id,
                text=input_text,
                status="extracted", # Or 'pending_triage'
                created_at=datetime.now() # Use Python's datetime for consistency or func.now() from DB side
            )
            db_session.add(new_note)
            db_session.commit()
            print(f"Original note linked to Patient ID {new_patient.patient_id} and saved as Note ID {new_note.note_id}.")


        except IntegrityError as e:
            db_session.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                print(f"\nError: A patient with NHS Number '{nhs_number}' already exists. NHS Number must be unique.")
            else:
                print(f"\nDatabase Integrity Error: {e}")
        except Exception as e:
            db_session.rollback()
            print(f"\nAn unexpected error occurred during database operation: {e}")

    except Exception as e:
        print(f"An error occurred during LLM processing: {e}")

# --- Main execution loop ---
if __name__ == "__main__":
    print("Welcome! Enter patient medical notes to extract and store data.")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        print("\n------------------------------------------------")
        input_text = input("Enter patient note text:\n")
        if input_text.lower() in ['exit', 'quit']:
            break

        extract_and_process_patient_data(input_text)

    db_session.close()
    print("Database session closed. Exiting.")