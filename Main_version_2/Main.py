from triage import triage_rules
import openai
from dotenv import load_dotenv
load_dotenv()
client = openai.OpenAI()

from classifier import get_semi_and_unstructured
from Ingester import ingesting_pdf
import json
from structured_data_to_json_format import extract_single_text_to_json, PatientDemographics

# If the file is in a subdirectory, use:
# from .Structured_data_to_JSON_format import extract_single_text_to_json


def etl_process(path: str):
    # Utilising ingesting function
    pages = ingesting_pdf(path)
    return pages


def structured_json_process(processed_text: str):
    patient_data_json_file = extract_single_text_to_json(processed_text)
    return patient_data_json_file


def preprocess_patient_text(patient_text: str) -> str:
    chunks = get_semi_and_unstructured(patient_text)
    return "\n\n".join(chunks)


def ai_triage(clean_text: str):
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a clinical triage assistant. Classify referrals strictly according to the following triage rules:

{json.dumps(triage_rules, indent=2)}

Based on the rules provided above, indicate the appropriate priority or Not Accepted if the referral is outside urology.
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
    # Changed Path of sample document, please tell if broken
    sample_document_path = "Main_version_2/sample.pdf"

    # Extract text from pdf and adding to processed_text variable
    processed_text = etl_process(sample_document_path)

    print("\nStructured JSON Output:")
    structured_json_file = structured_json_process(processed_text)
    print(structured_json_file)

    print("\nAI Triage Output:")
    ai_triage_output = ai_triage(processed_text)
    print(ai_triage_output)

    # Printing pdf information for now
    # print(processed_text)
