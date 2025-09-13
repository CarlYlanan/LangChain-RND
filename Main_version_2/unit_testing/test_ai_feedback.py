import json
import pytest
from unittest.mock import patch, mock_open
from Main_version_2.ai_feedback import loading_memory, accepting_feedback, build_feedback_examples

# Test: loading_memory when file doesn't exist
@patch("Main_version_2.ai_feedback.os.path.exists", return_value=False)
@patch("Main_version_2.ai_feedback.open", new_callable=mock_open)
@patch("Main_version_2.ai_feedback.json.dump")
def test_loading_memory_creates_file(mock_json_dump, mock_open_fn, mock_exists):
    result = loading_memory()
    assert result == []
    mock_json_dump.assert_called_once_with([], mock_open_fn())

# Test: loading_memory when file is empty
@patch("Main_version_2.ai_feedback.os.path.exists", return_value=True)
@patch("Main_version_2.ai_feedback.os.path.getsize", return_value=0)
def test_loading_memory_empty_file(mock_getsize, mock_exists):
    result = loading_memory()
    assert result == []

# Test: loading_memory with existing data
@patch("Main_version_2.ai_feedback.os.path.exists", return_value=True)
@patch("Main_version_2.ai_feedback.os.path.getsize", return_value=10)
@patch("Main_version_2.ai_feedback.open", new_callable=mock_open, read_data='[{"feedback": "Good"}]')
def test_loading_memory_with_data(mock_open_fn, mock_getsize, mock_exists):
    result = loading_memory()
    assert isinstance(result, list)
    assert result[0]["feedback"] == "Good"

# Test: accepting_feedback appends and writes
@patch("Main_version_2.ai_feedback.loading_memory", return_value=[])
@patch("Main_version_2.ai_feedback.open", new_callable=mock_open)
@patch("Main_version_2.ai_feedback.json.dump")
def test_accepting_feedback(mock_json_dump, mock_open_fn, mock_loading):
    accepting_feedback("file.pdf", "AI output", "Helpful", "Accepted")
    args, kwargs = mock_json_dump.call_args
    assert isinstance(args[0], list)
    assert args[0][0]["file_name"] == "file.pdf"

# Test: build_feedback_examples formats correctly
def test_build_feedback_examples_formatting():
    memory = [{
        "file_name": "doc.pdf",
        "ai_triage_output": "Summary\n\nDetails here.",
        "feedback": "Needs clarification.",
        "final_decision": "Rejected"
    }]
    result = build_feedback_examples(memory)
    assert "Referral summary: Summary" in result
    assert "Feedback: Needs clarification." in result
    assert "Final decision: Rejected" in result
