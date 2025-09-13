import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from Main_version_2.ingester import ingesting_pdf

# Helpers
def make_pdf_file(tmp_path, name="sample.pdf", content="This is a fake PDF text."):
    """Create a dummy .pdf file in temp directory (not a real PDF, just placeholder)."""
    pdf_path = tmp_path / name
    pdf_path.write_text(content)
    return str(pdf_path)

# --- Test: Single PDF file ---
@patch("Main_version_2.ingester.PyPDFLoader")
def test_single_pdf_file(mock_loader, tmp_path):
    pdf_path = make_pdf_file(tmp_path, "single.pdf")

    # Mock loader output
    mock_doc = MagicMock()
    mock_doc.page_content = "Mocked PDF content"
    mock_loader.return_value.load.return_value = [mock_doc]

    result = ingesting_pdf(pdf_path)

    assert len(result) == 1
    assert result[0][0] == "single.pdf"
    assert "Mocked PDF content" in result[0][1]

# --- Test: Multiple PDFs in folder ---
@patch("Main_version_2.ingester.PyPDFLoader")
def test_multiple_pdfs_in_folder(mock_loader, tmp_path):
    pdf1 = make_pdf_file(tmp_path, "a.pdf")
    pdf2 = make_pdf_file(tmp_path, "b.pdf")

    mock_doc1 = MagicMock()
    mock_doc1.page_content = "Doc1 content"
    mock_doc2 = MagicMock()
    mock_doc2.page_content = "Doc2 content"

    mock_loader.return_value.load.side_effect = [[mock_doc1], [mock_doc2]]

    result = ingesting_pdf(str(tmp_path))

    filenames = [r[0] for r in result]
    assert filenames == ["a.pdf", "b.pdf"]
    assert "Doc1 content" in result[0][1]
    assert "Doc2 content" in result[1][1]

# --- Test: Non-PDF file ---
def test_non_pdf_file(tmp_path):
    txt_path = tmp_path / "file.txt"
    txt_path.write_text("Hello, not a PDF")

    result = ingesting_pdf(str(txt_path))
    assert result == []

# --- Test: Invalid path ---
def test_invalid_path():
    result = ingesting_pdf("this/path/does/not/exist.pdf")
    assert result == []
