import json
import openai
import os
from dotenv import load_dotenv
from hashing import hash_sensitive_info
from Ingester import ingesting_pdf
from structured_data_to_json_format import extract_single_text_to_json, PatientDemographics
from classifier import get_semi_and_unstructured
from triage import triage_rules
from sqlalchemy import create_engine
from ai_feedback import loading_memory, accepting_feedback, get_feedback_context
from models import Base, ReferralTriageResult


load_dotenv()
client = openai.OpenAI()

def init_db():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not set in environment.")
    
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Table `referral_triage_results` has been created or already exists.")


# For performance metrics
import time
start_time = time.time()

# if the file is in a subdirectory, use:
# from .Structured_data_to_JSON_format import extract_single_text_to_jsonpip

def etl_process(folder_path: str):
    return ingesting_pdf(folder_path)

def structured_json_process(processed_text: str):
    patient_data_json_file = extract_single_text_to_json(processed_text)
    return patient_data_json_file


def preprocess_patient_text(patient_text: str) -> str:
    chunks = get_semi_and_unstructured(patient_text)
    return "\n\n".join(chunks)  


def ai_triage(clean_text: str, file_name: str):
    feedback_memory = get_feedback_context()
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a clinical triage assistant. Classify referrals strictly according to the following triage rules:

{json.dumps(triage_rules, indent=2)}

You also have memory from corrections made by past clinicians. Use them if relevant:
{feedback_memory}

Based on the rules provided above, indicate the appropriate priority or Not Accepted if the referral is outside urology.
Add a 2 sentence summary based on your decision making at the end, followed with the disclaimer below
Add this comment at the end: Disclaimer, this response has been generated utilising ChatGPT.

Output format should be exactly like this example (0 = no, 1 = yes):
Priority 1: 0 (reason, 1 line max)
Priority 2: 0 (reason, 1 line max)
Priority 3: 1 (reason, 1 line max)
Priority 4: 0 (reason, 1 line max)
Not Accepted: 0 (reason, 1 line max)
"""
            },
            {
                "role": "user",
                "content": f"""
    Patient referral details:
    {clean_text}

    Classify this referral strictly following the rules above. Provide output exactly.
    """
                }
            ],
            max_tokens=500,
            temperature=0
        )

    return response.choices[0].message.content


if __name__ == "__main__":
    init_db()
    # changed path to folder
    sample_folder_path = "sample_documents"

    # extract text from each PDF
    all_docs = etl_process(sample_folder_path)  # now returns list of (filename, text)


    for file_name, processed_text in all_docs:
        print(f"\n--- Processing: {file_name} ----------------------------------------")

        # extracting key data from structured section
        structured_json_file = structured_json_process(processed_text)
        #print("\nStructured JSON Output:")
        print(structured_json_file)
        
        # Hash sensitive info
        hashed_text = hash_sensitive_info(processed_text)
        
        # AI answer
        print("\nAI Triage Output:")
        ai_triage_output = ai_triage(hashed_text, file_name)
        print(ai_triage_output)
        
        
        # getting feedback from terminal
        #feedback = input("Enter feedback here (or press Enter if decision was correct): ")
        #final_result = input("Enter final result (Priority X / Not Accepted, or press Enter if same as AI): ")
        
        #if feedback.strip() or final_result.strip():
        #    accepting_feedback(file_name, ai_triage_output, feedback or "No feedback", final_result or ai_triage_output)
     
    #This is for performance metrics purposes
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")