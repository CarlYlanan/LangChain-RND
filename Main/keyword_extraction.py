from typing_extensions import TypedDict, Annotated
from typing import Optional
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from config import API_KEY





# Load environment variables
load_dotenv(dotenv_path=".env")
API_KEY = os.getenv("OPENAI_API_KEY")

# Define the schema using TypedDict and Annotated
class MedicalKeywordExtraction(TypedDict):
    patient_id: Annotated[str, "Patient identification or MRN"]
    diagnoses: Annotated[list[str], "Medical diagnoses mentioned in the report"]
    symptoms: Annotated[list[str], "Symptoms or issues that the patient is experiencing"]
    treatments: Annotated[list[str], "Treatments, interventions, or medical devices used"]

# Initialize the chat model with GPT-4 or GPT-4o
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Wrap the model into structured output using function calling
structured_llm = llm.with_structured_output(MedicalKeywordExtraction, method="function_calling")


def extract_keywords(input_text):
    response = structured_llm.stream(input_text)

    return (
        f"Patient ID: {response['patient_id']}\n\n"
        f"Diagnoses:\n" + "\n".join(response["diagnoses"]) + "\n\n"
        f"Symptoms:\n" + "\n".join(response["symptoms"]) + "\n\n"
        f"Treatments:\n" + "\n".join(response["treatments"])
    )


