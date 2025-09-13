import pytest
from unittest.mock import patch
from Main_version_2 import hashing

def test_hash_sensitive_info_basic():
    hashing.reset_usage_tracking()
    input_text = (
        "Patient name: John Doe\n"
        "NHS number: AB12345\n"
        "Phone: 021 123 4567\n"
        "Email: john.doe@example.com\n"
        "Hospital ID: HOSP001"
    )

    with patch.object(hashing, "FIRST_NAMES", ["Alice", "Bob"]), \
         patch.object(hashing, "LAST_NAMES", ["Smith", "Jones"]):
        output = hashing.hash_sensitive_info(input_text)

    # Ensure output is a string and contains no original identifiers
    assert isinstance(output, str)
    assert "John Doe" not in output
    assert "AB12345" not in output
    assert "021 123 4567" not in output
    assert "john.doe@example.com" not in output
    assert "HOSP001" not in output

    # Ensure fake data was generated and tracked
    stats = hashing.get_usage_statistics()
    assert stats["used_full_names"] == 1
    assert stats["used_phone_numbers"] >= 1
    assert stats["used_nhi_numbers"] >= 1

def test_reset_usage_tracking():
    hashing.USED_FULL_NAMES.add("Test Name")
    hashing.USED_PHONE_NUMBERS.add("1234567890")
    hashing.USED_NHI_NUMBERS.add("AB12345")
    hashing.reset_usage_tracking()
    assert len(hashing.USED_FULL_NAMES) == 0
    assert len(hashing.USED_PHONE_NUMBERS) == 0
    assert len(hashing.USED_NHI_NUMBERS) == 0

def test_get_usage_statistics_consistency():
    hashing.reset_usage_tracking()
    stats = hashing.get_usage_statistics()
    assert stats["used_full_names"] == 0
    assert stats["available_name_combinations"] > 0
