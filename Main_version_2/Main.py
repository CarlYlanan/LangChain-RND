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

if __name__ == "__main__":
    #Changed Path of sample document, please tell if broken
    sample_document_path = "Main_version_2/sample.pdf"

    #Extract text from pdf and adding to processed_text variable
    processed_text = etl_process(sample_document_path)

    
    print("\nStructured JSON Output:")
    structured_json_file=structured_json_process(processed_text)
    print(structured_json_file)

    
    #Printing pdf information for now
    #print(processed_text)