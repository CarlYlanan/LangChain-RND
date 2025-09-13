import pytest
from unittest.mock import patch, MagicMock
from Main_version_2.patient_details_to_db import extract_data_from_text, add_data_to_db

def test_extract_data_from_text_valid_input():
    sample_text = (
        "Patient Name: John Smith  \n"
        "Date of birth: 01/02/1980\n"
        "NHS number: 1234567890\n"
        "Hospital ID: HOSP001"
    )
    result = extract_data_from_text(sample_text)
    assert result["Patient Name"] == "John Smith"
    assert result["Date of Birth"] == "01/02/1980"
    assert result["NHS number"] == "1234567890"
    assert result["Hospital ID"] == "HOSP001"

def test_extract_data_from_text_missing_fields():
    sample_text = "Patient Name: Jane Doe  \nDate of birth:"
    result = extract_data_from_text(sample_text)
    assert result["Patient Name"] == "Jane Doe"
    assert result["Date of Birth"] is None
    assert result["NHS number"] is None
    assert result["Hospital ID"] is None

@patch("Main_version_2.patient_details_to_db.create_engine")
@patch("Main_version_2.patient_details_to_db.os.getenv", return_value="sqlite:///:memory:")
def test_add_data_to_db(mock_getenv, mock_create_engine):
    mock_engine = MagicMock()
    mock_connection = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_connection
    mock_create_engine.return_value = mock_engine

    extracted = {
        "Patient Name": "Alice",
        "Date of Birth": "02/03/1990",
        "NHS number": "9876543210",
        "Hospital ID": "HOSP999"
    }

    add_data_to_db(extracted, "source.pdf")

    assert mock_connection.execute.called
    assert mock_connection.commit.called
