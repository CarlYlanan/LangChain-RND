# tests/test_classifier.py
import pytest 
from unittest.mock import patch
from Main_version_2.classifier import (split_into_chunks, clean_structured_chunk, 
classify_chunk,
split_document_sections_by_chunks,
get_semi_and_unstructured)

# Tests for split_into_chunks
def test_split_into_chunks_basic():
    text = "Line one.\n\nLine two.\n\n\nLine three."
    chunks = split_into_chunks(text)
    assert chunks == ["Line one.", "Line two.", "Line three."]

def test_split_into_chunks_min_words():
    text = "Hi\n\nA very short paragraph\n\nAnother"
    chunks = split_into_chunks(text, min_words=2)
    assert chunks == ["A very short paragragh"]

# Tests for clean_structured_chunk
def test_clean_structured_chunk_merges_label_lines():
    input_chunk = "Patient Name:\nJohn Doe\nDate of Birth:\n01/01/1980\nNotes:\nPatients is well."
    expected = "Patient Name: John Doe\nDate of Birth: 01/01/1980\nNotes:\nPatient is well."
    assert clean_structured_chunk(input_chunk) == expected

def test_clean_structured_chunk_preserves_normal_lines():
    input_chunk = "General Info:\nAll clear.\nNo issues."
    expected = "General Info:\nAll clear.\nNo issues."
    assert clean_structured_chunk(input_chunk) == expected

# Tests for classify_chunk (mocked)
def test_classify_chunk_mocked():
    class MockResponse:
        def __init__(self, content):
            self.content = content

    with patch("Main_version_2.classifier.classifier_chain.invoke", return_value=MockResponse("structured")):
        result = classify_chunk("Some text")
        assert result == "structured"

# Tests for split_document_sections_by_chunks (mocked)
def test_split_document_sections_by_chunks_mocked():
    text = "Patient Name:\nJohn Doe\n\nSemi-structured note.\n\nFree text observation."

    with patch("Main_version_2.classifier.classify_chunk") as mock_classify:
        mock_classify.side_effect = ["structured", "semi-structured", "unstructured"]

        sections = split_document_sections_by_chunks(text)

        assert len(sections["structured"]) == 1
        assert len(sections["semi-structured"]) == 1
        assert len(sections["unstructured"]) == 1

# Tests for get_semi_and_unstructured (mocked)
def test_get_semi_and_unstructured_mocked():
    text = "Structured chunk.\n\nSemi-structured note.\n\nFree text observation."

    with patch("Main_version_2.classifier.classify_chunk") as mock_classify:
        mock_classify.side_effect = ["structured", "semi-structured", "unstructured"]

        result = get_semi_and_unstructured(text)

        assert len(result) == 2
        assert "Semi-structured note." in result[0]
        assert "Free text observation." in result[1]

