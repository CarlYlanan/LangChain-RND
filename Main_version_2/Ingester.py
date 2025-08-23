#Importing PdfReader to read sample documents
from langchain_community.document_loaders import PyPDFLoader
import os
#Creating function for ingesting pdf with parameter of "path"
"""
def ingesting_pdf(path: str):
    #Loading pdf via parameter provided
    loader = PyPDFLoader(path)
    
    #Loading all referral pages from pdf into documents
    documents = loader.load()
    
    #Covnerting frrom a document object to a string 
    referral_text = "\n\n".join([doc.page_content for doc in documents])
        
    return referral_text



def ingesting_pdf(folder_path: str):
    combined_texts = []

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, file_name)
            loader = PyPDFLoader(full_path)
            documents = loader.load()
            referral_text = "\n\n".join([doc.page_content for doc in documents])
            combined_texts.append((file_name, referral_text))
    
    return combined_texts  # returns list of (filename, text) tuples

"""



def ingesting_pdf(path: str):
    """
    If `path` is a folder: returns list[(filename, text), ...] for all *.pdf (sorted).
    If `path` is a single PDF: returns [(filename, text)].
    Otherwise: returns [].
    """
    results = []

    if os.path.isdir(path):
        for file_name in sorted(os.listdir(path)):
            if file_name.lower().endswith(".pdf"):
                full_path = os.path.join(path, file_name)
                loader = PyPDFLoader(full_path)
                docs = loader.load()
                text = "\n\n".join(doc.page_content for doc in docs)
                results.append((file_name, text))
        return results

    # Handle single-PDF input
    if os.path.isfile(path) and path.lower().endswith(".pdf"):
        file_name = os.path.basename(path)
        loader = PyPDFLoader(path)
        docs = loader.load()
        text = "\n\n".join(doc.page_content for doc in docs)
        return [(file_name, text)]

    # Nothing usable found
    return []
