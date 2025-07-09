import pytest
from clean_text import clean_text


def test_remove_unwanted_characters():
    input_text = "Hello! This is @test #string with $weird^chars*~."
    expected = "Hello This is @test string with weirdchars."
    assert clean_text(input_text) == expected

def test_preserve_allowed_punctuation():
    input_text = "Note: Patient's temperature is 37.5°C (normal range: 36.5—37.5)."
    expected = "Note: Patient's temperature is 37.5C (normal range: 36.537.5)."

def test_collapse_spaces():
    input_text = "This    is   a   test."
    expected = "This is a test."
    assert clean_text(input_text) == expected

def test_preserve_newlines():
    input_text = "Line one.   \n   Line two.\n\nLine    three."
    expected = "Line one.\nLine two.\n\nLine three."
    assert clean_text(input_text) == expected

def test_empty_string():
    assert clean_text("") == ""
