from ingester import ingesting_pdf
from clean_text import clean_text
from normalise_text import normalise_text
from extraction import extract_keywords
from classifier import run_classification_pipeline
from typing_extensions import TypedDict, Annotated

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


if __name__ == "__main__":
    sample_document_path = "../sample_documents/sample1.pdf"

    #Extract, clean, normalise
    processed_text = etl_process(sample_document_path)

    #Run classification on cleaned text
    run_classification_pipeline(processed_text)
