import pytest
from unittest.mock import MagicMock
from keyword_extraction import extract_keywords, structured_llm
from config import API_KEY

@pytest.fixture
def mock_llm_response():
    return {
        "patient_id": "12345",
        "diagnoses": ["Diabetes", "Hypertension"],
        "symptoms": ["Fatigue", "Blurred vision"],
        "treatments": ["Insulin", "Lifestyle changes"]
    }

def test_extract_keywords(monkeypatch, mock_llm_response):
    # Mock the stream method
    monkeypatch.setattr(type(structured_llm), "stream", MagicMock(return_value=mock_llm_response))


    input_text = (
        "Patient 12345 has diabetes and hypertension. "
        "Complains of fatigue and blurred vision. "
        "Prescribed insulin and advised lifestyle changes."
    )

    expected_output = (
        "Patient ID: 12345\n\n"
        "Diagnoses:\nDiabetes\nHypertension\n\n"
        "Symptoms:\nFatigue\nBlurred vision\n\n"
        "Treatments:\nInsulin\nLifestyle changes"
    )

    result = extract_keywords(input_text)
    assert result == expected_output

