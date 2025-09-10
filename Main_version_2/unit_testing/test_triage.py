import pytest
from Main_version_2.triage import triage_rules  # adjust path if needed

def test_all_priorities_present():
    expected_keys = {"Priority 1", "Priority 2", "Priority 3", "Priority 4", "Not Accepted"}
    assert set(triage_rules.keys()) == expected_keys

def test_required_fields_exist():
    for priority, rule in triage_rules.items():
        assert "label" in rule
        assert "target_timeframe" in rule
        assert "examples" in rule
        assert "trigger_terms" in rule
        assert "rationale" in rule

def test_trigger_terms_are_non_empty_strings():
    for rule in triage_rules.values():
        for term in rule["trigger_terms"]:
            assert isinstance(term, str)
            assert term.strip() != ""

def test_examples_are_non_empty_strings():
    for rule in triage_rules.values():
        for example in rule["examples"]:
            assert isinstance(example, str)
            assert example.strip() != ""

def test_priority_labels_are_unique():
    labels = [rule["label"] for rule in triage_rules.values()]
    assert len(labels) == len(set(labels))  # no duplicates

def test_not_accepted_has_na_timeframe():
    assert triage_rules["Not Accepted"]["target_timeframe"] == "N/A"
