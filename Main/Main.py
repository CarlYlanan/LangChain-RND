from ingester import ingesting_pdf

def etl_process(path: str):
    pages = ingesting_pdf(path)

if __name__ == "__main__":
    sample_document_path = "../sample_documents/sample1.pdf"
    etl_process(sample_document_path)