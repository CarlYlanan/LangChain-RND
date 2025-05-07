#Importing PdfReader to read sample documents
from langchain.document_loaders import PyPDFLoader

#Providing path to pdf file
loader1 = PyPDFLoader("../sample_documents/sample1.pdf")
pages = loader1.load()

#Loop through all pages within pdf and printing out its context
for page in pages:
    #Printing content within pdf file to terminal for now
    print(page.page_content)
