from Ingester import ingesting_pdf

def etl_process(path: str):
    #Utilising ingesting function
    pages = ingesting_pdf(path)
    
    #Returning pages ingested 
    return pages


if __name__ == "__main__":
    #Changed Path of sample document, please tell if broken
    sample_document_path = "Main_version_2/sample.pdf"

    #Extract text from pdf and adding to processed_text variable
    processed_text = etl_process(sample_document_path)
    
    #Printing pdf information for now
    print(processed_text)