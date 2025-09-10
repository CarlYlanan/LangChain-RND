import json
import pytest
from unittest.mock import patch, MagicMock, mock_open
from Main_version_2.structured_data_to_json_format import extract_single_text_to_json, PatientDemographics

@patch("Main_version_2.structured_data_to_json_format.ChatOpenAI")
@patch("Main_version_2.structured_data_to_json_format.open", new_callable=mock_open)
@patch("Main_version_2.structured_data_to_json_format.load_dotenv")
@patch("Main_version_2.structured_data_to_json_format.os.getenv", return_value="fake-key")
def test_extract_single_text_to_json(mock_getenv, mock_load_dotenv, mock_open_fn, mock_chat_model):

    # Mock the structured LLM and its stream output
    mock_llm_instance = MagicMock()
    mock_llm_instance.with_structured_output.return_value.stream.return_value = [
        {
            "name": "Jane Doe",
            "dob": "1990-12-01",
            "gender": "Female",
            "nhs_number": "1234567890",
            "phone_number": "07123456789",
            "email": "jane@example.com",
            "pregnancy": False
        }
    ]
    mock_chat_model.return_value = mock_llm_instance

    input_text = "Patient is Jane Doe, born 1990-12-01, NHS number 1234567890, not pregnant."
    result = extract_single_text_to_json(input_text, output_file="dummy.json")

    # Validate result structure
    assert isinstance(result, dict)
    assert result["name"] == "Jane Doe"
    assert result["pregnancy"] is False

    # Validate file write
    mock_open_fn.assert_called_once_with("dummy.json", "w", encoding="utf-8")
    handle = mock_open_fn()
    handle.write.assert_called()  # Ensures json.dump was called
