#Importing PdfReader to read sample documents
from langchain_community.document_loaders import PyPDFLoader

#Creating function for ingesting pdf with parameter of "path"
def ingesting_pdf(path: str):
    #Loading pdf via parameter provided
    loader = PyPDFLoader(path)
    
    #Loading all referral pages from pdf into documents
    documents = loader.load()
    
    #Covnerting frrom a document object to a string 
    referral_text = "\n\n".join([doc.page_content for doc in documents])
        
    return referral_text

    