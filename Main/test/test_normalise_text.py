import pytest
from normalise_text import normalise_text

def test_normalise_mixed_case():
    input_text = "PaTient in DENial of Her Disease."
    expected = "patient in denial of her disease."
    assert normalise_text(input_text) == expected

def test_normalise_basic_text():
    assert normalise_text("HELLO WORLD") == "hello world"

def test_normalise_with_numbers():
    assert normalise_text("Score: 98% Passed") == "score: 98% passed"

def test_normalise_with_symbols():
    assert normalise_text("This & That!") == "this & that!"

def test_normalise_empty_string():
    assert normalise_text("") == ""