import os
from typing_extensions import TypedDict, Annotated
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Define the schema using TypedDict and Annotated
class MedicalKeywordExtraction(TypedDict):
    patient_id: Annotated[str, "Patient identification or NHI"]
    diagnoses: Annotated[list[str], "Medical diagnoses mentioned in the report"]
    symptoms: Annotated[list[str], "Symptoms or issues the patient is experiencing"]
    treatments: Annotated[list[str], "Treatments, interventions, or medical devices used"]

# Function to extract medical keywords from a text string
def extract_medical_keywords_from_text(text: str) -> MedicalKeywordExtraction | None:
    """Extracts structured medical keywords from a given text string."""

    
    
    # Initialize the chat model and wrap it with structured output
    llm = ChatOpenAI(temperature=0)
    structured_llm = llm.with_structured_output(MedicalKeywordExtraction)

    try:
        result = structured_llm.invoke(text)
        return result
    except Exception as e:
        print(f"Error processing text: {e}")
        return None


sample_text = """Patient ID: NHI12345. The patient reports persistent headaches and blurred vision.
Diagnosed with hypertension and type 2 diabetes. Currently on metformin and using a CPAP machine at night.
    """    
extracted_data = extract_medical_keywords_from_text(sample_text)
print(extracted_data)





