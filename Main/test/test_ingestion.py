import pytest
from Main.ingester import ingesting_pdf

#Paths to correct and corrupt sample pdfs
correct_pdf_path = "sample_documents/sample1.pdf"
corrupt_pdf_path = "../sample_documents/sample2.pdf"

#Testing correct sample document 
def test_correct_sample():
    docs = ingesting_pdf(correct_pdf_path)
    assert isinstance(docs, list)
    assert len(docs) > 0
    assert any("Patient" in doc.page_content and 
               "Diagnoses" in doc.page_content and 
               "GP" in doc.page_content in doc.page_content for doc in docs)

#Testing corrupt sample document
def test_corrupt_sample():
    with pytest.raises(Exception):
        ingesting_pdf(corrupt_pdf_path)
        
#To test this file run: PYTHONPATH=Main python3 -m pytest Main/test/test_ingestion.py (in the LangChain-RND directory)