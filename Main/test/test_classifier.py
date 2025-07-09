import pytest
from Main.classifier import split_into_chunks, clean_structured_chunk

def test_split_into_chunks_basic():
    text = "Line one.\n\nLine two.\n\n\nLine three."
    chunks = split_into_chunks(text)
    assert chunks == ["Line one.", "Line two.", "Line three."]

def test_split_into_chunks_min_words():
    text = "Hi\n\nA very short paragraph\n\nAnother"
    chunks = split_into_chunks(text, min_words=2)
    assert chunks == ["A very short paragraph"]

def test_clean_structured_chunk_merges_label_lines():
    input_chunk = "Patient Name:\nJohn Doe\nDate of Birth:\n01/01/1980\nNotes:\nPatient is well."
    expected = "Patient Name: John Doe\nDate of Birth: 01/01/1980\nNotes:\nPatient is well."
    assert clean_structured_chunk(input_chunk) == expected

def test_clean_structured_chunk_preserves_normal_lines():
    input_chunk = "General Info:\nAll clear.\nNo issues."
    expected = "General Info:\nAll clear.\nNo issues."
    assert clean_structured_chunk(input_chunk) == expected