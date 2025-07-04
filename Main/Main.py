from ingester import ingesting_pdf
from clean_text import clean_text
from normalise_text import normalise_text
from keyword_extraction import extract_keywords
from classifier import run_classification_pipeline
from typing_extensions import TypedDict, Annotated

from database import insert_validated_med_results
from datetime import datetime

# Define the schema using TypedDict and Annotated
class MedicalKeywordExtraction(TypedDict):
    patient_id: Annotated[str, "Patient identification or NHI"]
    diagnoses: Annotated[list[str], "Medical diagnoses mentioned in the report"]
    symptoms: Annotated[list[str], "Symptoms or issues the patient is experiencing"]
    treatments: Annotated[list[str], "Treatments, interventions, or medical devices used"]


def etl_process(path: str):
    #Utilising ingesting function
    pages = ingesting_pdf(path)
    
    #Loop through all pages within pdf and storing cleaned text into a list
    cleaned_data = []
    for page in pages:
        cleaned = clean_text(page.page_content)
        cleaned_data.append(cleaned)
        
    total_cleaned_data =  '\n\n'.join(cleaned_data)
    
    #Normalising all cleaned data, changing text to all lowercase 
    normalised_data = normalise_text(total_cleaned_data)
    
    #Extracting all the keywords from the cleaned and normalised data
    extracted_keywords_results = extract_keywords(normalised_data)
    
    return extracted_keywords_results


def save_to_database(classified_results: list[dict], source_path: str):
    formatted_records = []

    for item in classified_results:
        record = {
            "patient_name": "Unknown",  # replace if available in `item`
            "date_of_birth": None,
            "date_of_appointment": datetime.now(),
            "nhs_number": item.get("patient_id", "MISSING_NHS"),
            "hospital_id": None,
            "address": None,
            "email": None,
            "medical_staff": None,
            "symptoms": ', '.join(item.get("symptoms", [])),
            "diagnosis": ', '.join(item.get("diagnoses", [])),
            "treatment_plan": ', '.join(item.get("treatments", [])),
            "urgency_value": "Medium",
            "record_status": "Active",
            "source_document": source_path,
        }

        formatted_records.append(record)

    insert_validated_med_results(formatted_records)

if __name__ == "__main__":
    sample_document_path = "../sample_documents/sample1.pdf"

    #Extract, clean, normalise
    processed_text = etl_process(sample_document_path)

    #Run classification on cleaned text
    run_classification_pipeline(processed_text)

    #Save classified results to database
    save_to_database(processed_text, sample_document_path)
