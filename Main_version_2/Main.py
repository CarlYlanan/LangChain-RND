from triage import triage_rules
import openai
from dotenv import load_dotenv
load_dotenv()
client = openai.OpenAI()
from classifier import get_semi_and_unstructured


from Ingester import ingesting_pdf
import json
# Ensure the module exists in the same directory or update the import path accordingly
# Example if the file is in the same directory:
from structured_data_to_json_format import extract_single_text_to_json, PatientDemographics

# If the file is in a subdirectory, use:
# from .Structured_data_to_JSON_format import extract_single_text_to_json

def etl_process(path: str):
    #Utilising ingesting function
    pages = ingesting_pdf(path)
    
    #Returning pages ingested 
    return pages

def structured_json_process(processed_text: str):
    patient_data_json_file=extract_single_text_to_json(processed_text)

    return patient_data_json_file



def preprocess_patient_text(patient_text: str) -> str:
    chunks = get_semi_and_unstructured(patient_text)
    return "\n\n".join(chunks)

def ai_triage(clean_text: str):
    prompt = f"""{triage_rules}

Using the above Urology Referral Grading Matrix rules, analyze the following patient referral details and determine the appropriate referral category (Priority 1, 2, 3, 4 or Return to GP). Provide a brief rationale for your decision.

Patient referral details:
{clean_text}

Response format:
Referral Category: <Priority 1/2/3/4/Return to GP>
Rationale: <Explain why>
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": triage_rules},
            {"role": "user", "content": clean_text},
            {"role": "assistant", "content": "Please categorize this referral according to the rules and explain."}
        ],
        max_tokens=500,
        temperature=0
    )
    return response.choices[0].message.content



if __name__ == "__main__":
    #Changed Path of sample document, please tell if broken
    sample_document_path = "Main_version_2/sample.pdf"

    #Extract text from pdf and adding to processed_text variable
    processed_text = etl_process(sample_document_path)

    
    print("\nStructured JSON Output:")
    structured_json_file=structured_json_process(processed_text)
    print(structured_json_file)

    print("\nAI Triage Output:")
    ai_triage_output = ai_triage(processed_text)
    print(ai_triage_output)

    
    #Printing pdf information for now
    #print(processed_text)
