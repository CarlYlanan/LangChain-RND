#Importing PdfReader to read sample documents
from PyPDF2 import PdfReader

#Providing path to pdf file
reader1 = PdfReader("../sample_documents/sample1.pdf")

#Loop through all pages within pdf and printing out its context
for page_num in range(len(reader1.pages)):
    #Extract info from each page 
    page = reader1.pages[page_num]
    
    #Printing text within pdf file to terminal for now
    print(page.extract_text())
