import json
import openai
import os
from dotenv import load_dotenv
from hashing import hash_sensitive_info
from Ingester import ingesting_pdf
from classifier import get_semi_and_unstructured
from triage import triage_rules
from sqlalchemy import create_engine
from ai_feedback import loading_memory, accepting_feedback, build_feedback_examples
from models import Base, ReferralTriageResult
from structured_json_to_table import extract_data_from_text
from structured_json_to_table import add_data_to_db

# Loading .env file
load_dotenv()
# Initialising client object to interact with OpenAI API
client = openai.OpenAI()

# Initialise referral_triage_results database   
def init_db():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not set in environment.")
    
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    #print("Table `referral_triage_results` has been created or already exists.")

# Starting time to measure performance metrics
import time
start_time = time.time()

# Function to ingest the referral pdfs 
def referral_ingestion(folder_path: str):
    return ingesting_pdf(folder_path)

# Function that extracts personal details and adds them into our database table
def personal_info_insertion_to_db(processed_text: str, source_filename: str):

    # This now correctly receives only one item (the dictionary)
    extracted_data = extract_data_from_text(processed_text)

   
    # This function call is now correct
    add_data_to_db(extracted_data, source_filename)
    
    return (extracted_data, source_filename)

# Classifying pdf into sections
# Excluding personal details from referrals
def preprocess_patient_text(patient_text: str) -> str:
    chunks = get_semi_and_unstructured(patient_text)
    return "\n\n".join(chunks)  

# Passing triaging rules and referrals to AI to provide priority decisions
def ai_triage(clean_text: str, file_name: str, dob: str=None):
    # loading in memory from feedback_memory.json
    feedback_memory_data = loading_memory()
    
    # Building examples from feedback memory for the AI to properly understand
    feedback_examples = build_feedback_examples(feedback_memory_data)

    # Getting the age of the patient
    dob_text = f"Date of Birth: {dob}\n" if dob else ""
    
    # Call the OpenAI chat model to classify the referral
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a clinical triage assistant. Classify referrals strictly according to the following triage rules:

{json.dumps(triage_rules, indent=2)}

Here are previous cases with corrections from clinicians:
{feedback_examples}

CRITICAL: Follow this decision process:
1. FIRST: Is this actually urology? (If other specialty mentioned → Not Accepted)
2. SECOND: What's the urgency level?
3. THIRD: Check against learned patterns above

IMPORTANT: If past feedback indicates that similar symptoms or cases were outside urology, classify accordingly as Not Accepted, even if the symptoms are moderate.

Based on the rules provided above, indicate the appropriate priority or Not Accepted if the referral is outside urology.
Add a 2 sentence summary based on your decision making at the end, followed with the disclaimer below
Add this comment at the end: Disclaimer, this response has been generated utilising ChatGPT.

Output format should be exactly like this example (0 = no, 1 = yes):
Priority 1: 0 (reason, one line max)
Priority 2: 0 (reason, one line max)
Priority 3: 1 (reason, one line max)
Priority 4: 0 (reason, one line max)
Not Accepted: 0 (reason, one line max)
"""
            },
            {
                "role": "user",
                "content": f"""
    Patient referral details:
    {dob_text}{clean_text}

    Classify this referral strictly following the rules above. Provide output exactly.
    """
                }
            ],
            max_tokens=500,
            temperature=0
        )

    return response.choices[0].message.content

if __name__ == "__main__":
    # Skipping database init
    # init_db()

    # Path to folder containing clinical referrals
    sample_folder_path = "sample_documents"

    # Ingesting documents and extracting all contents from each pdf 
    all_docs = referral_ingestion(sample_folder_path)

    for file_name, processed_text in all_docs:
        print(f"\n--- Processing: {file_name} ----------------------------------------")

        # Instead of inserting to DB, just simulate extracted personal info
        structured_json_file = {
            "Name": "Dummy Name",
            "Date of Birth": "01/01/1970"
        }
        dob = structured_json_file.get("Date of Birth")
        print("\Processed")
        print(processed_text)

        # Hash sensitive info
        hashed_text = hash_sensitive_info(processed_text)
        print("\n\nHashed Text:")
        print(hashed_text)



        # Classifying pdfs by extracting semi-structured and unstructured chunks from the hashed text
        semi_and_unstructured_chunks = get_semi_and_unstructured(hashed_text)
        semi_unstructured_text = "\n\n".join(semi_and_unstructured_chunks)

        # Passing information to our AI triaging algorithm
        #print("\nAI Triage Output:")
        ai_triage_output = ai_triage(semi_unstructured_text, file_name, dob=dob)
        print(ai_triage_output)

        #feedback=input("Enter feedback here (or press Enter if decision was correct):")
        #final_result=input("Enter final result (Priority X/Not Accepted, or press Enter if same as AI):")

        #if feedback.strip() or final_result.strip():
            #accepting_feedback(file_name, ai_triage_output, feedback or "No feedback", final_result or ai_triage_output)
        #else:
            #print("Acknowledged. No feedback saved.")                
            
        
    # Stopping timer for performance metrics
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
