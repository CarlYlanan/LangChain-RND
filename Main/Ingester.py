#Importing PdfReader to read sample documents
from langchain.document_loaders import PyPDFLoader

#Creating function for ingesting pdf with parameter of "path"
def ingesting_pdf(path: str):
    #Lodaing pdf via parameter provided
    loader = PyPDFLoader(path)
    return loader.load()
