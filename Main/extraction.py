from typing_extensions import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Define the schema using TypedDict and Annotated
class MedicalKeywordExtraction(TypedDict):
    patient_id: Annotated[str, "Patient identification or NHI"]
    diagnoses: Annotated[list[str], "Medical diagnoses mentioned in the report"]
    symptoms: Annotated[list[str], "Symptoms or issues the patient is experiencing"]
    treatments: Annotated[list[str], "Treatments, interventions, or medical devices used"]

# Initialize the chat model and wrap it with structured output
llm = ChatOpenAI(temperature=0)
structured_llm = llm.with_structured_output(MedicalKeywordExtraction)

# Function to extract medical keywords from a list of LangChain documents
def extract_keywords(text: str) -> Optional[str]:
    try:
        result: MedicalKeywordExtraction = structured_llm.invoke(text)
        
        # Convert the dict result to a nicely formatted string
        if result is None:
            return None

        output_str = (
            f"Patient ID: {result['patient_id']}\n\n"
            f"Diagnoses:\n" + "\n".join(result['diagnoses']) + "\n\n"
            f"Symptoms:\n" + "\n".join(result['symptoms']) + "\n\n"
            f"Treatments:\n" + "\n".join(result['treatments'])
        )
        
        return output_str
    except Exception as e:
        print(f"Error processing text: {e}")
        return None
