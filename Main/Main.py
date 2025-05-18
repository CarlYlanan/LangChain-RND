from ingester import ingesting_pdf
from clean_text import clean_text
from normalise_text import normalise_text

def etl_process(path: str):
    #Utilising ingesting function
    pages = ingesting_pdf(path)

    #Loop through all pages within pdf and storing cleaned text into a list
    cleaned_data = []
    for i, page in enumerate(pages):
        cleaned = clean_text(page.page_content)
        cleaned_data.append(cleaned)
        
    total_cleaned_data =  '\n\n'.join(cleaned_data)
    
    #Normalising all cleaned data, changing text to all lowercase 
    normalised_data = normalise_text(total_cleaned_data)
    #Testing if normalisation was executed successfully
    print(normalised_data)
    return normalised_data 

if __name__ == "__main__":
    sample_document_path = "../sample_documents/sample1.pdf"
    etl_process(sample_document_path)