from typing import Optional, List
from typing_extensions import TypedDict, Annotated

class PatientDemographics(TypedDict):
    """Information about the patient's identity and demographics."""
    name: Annotated[str, "The patient's full name."]
    dob: Annotated[Optional[str], "The patient's date of birth in YYYY-DD-MM format."]
    gender: Annotated[Optional[str], "The patient's gender (e.g., 'Male', 'Female', 'Other')."]
    nhs_number: Annotated[str, "The patient's NHS number. This is a mandatory and unique identifier."]
    phone_number: Annotated[Optional[str], "The patient's phone number."]
    email: Annotated[Optional[str], "The patient's email address."]
    pregnancy: Annotated[Optional[bool], "True if the patient is pregnant, False otherwise. Infer from context if not explicitly stated. If unknown, leave as None."]

class MedicalKeywordExtraction(TypedDict):
    """Structured extraction of key medical information from a clinical note."""
    demographics: PatientDemographics
    diagnoses: Annotated[List[str], "Medical diagnoses mentioned in the report"]
    symptoms: Annotated[List[str], "Symptoms or issues that the patient is experiencing"]
    treatments: Annotated[List[str], "Treatments, interventions, or medical devices used"]