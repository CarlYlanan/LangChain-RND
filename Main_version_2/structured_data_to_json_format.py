from typing import Optional, List
from typing_extensions import TypedDict, Annotated
import json
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
# from config import API_KEY

class PatientDemographics(TypedDict):
    """Information about the patient's identity and demographics."""
    name: Annotated[str, "The patient's full name."]
    dob: Annotated[Optional[str], "The patient's date of birth in YYYY-DD-MM format."]
    gender: Annotated[Optional[str], "The patient's gender (e.g., 'Male', 'Female', 'Other')."]
    nhs_number: Annotated[str, "The patient's NHS number. This is a mandatory and unique identifier."]
    phone_number: Annotated[Optional[str], "The patient's phone number."]
    email: Annotated[Optional[str], "The patient's email address."]
    pregnancy: Annotated[Optional[bool], "True if the patient is pregnant, False otherwise. Infer from context if not explicitly stated. If unknown, leave as None."]

def extract_single_text_to_json(input_text: str, output_file: str = "patient_data.json") -> PatientDemographics:
    # Load environment variables
    load_dotenv(dotenv_path=".env")
    API_KEY = os.getenv("OPENAI_API_KEY")

    # Initialize the chat model with GPT-4 or GPT-4o
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # Wrap the model into structured output using function calling
    structured_llm = llm.with_structured_output(PatientDemographics, method="function_calling")
    last_response = None
    for partial_response in structured_llm.stream(input_text):
        last_response = partial_response

    if last_response is None:
        raise ValueError("No response from LLM")

    # Save to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(last_response, f, indent=4)

    # Print the saved JSON
    print("Saved JSON content:")
    print(json.dumps(last_response, indent=4))

    return last_response
