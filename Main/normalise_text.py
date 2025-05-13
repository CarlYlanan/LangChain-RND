from langchain_community.document_loaders import PyPDFLoader

def normalise_text(text: str) -> str:
    """
    Converts all text to lowercase.
    """
    return text.lower()

# Importing pdfreader to read sample documents
loader1 = PyPDFLoader("sample_documents/sample1.pdf")
pages = loader1.load()

# Loop through all pages within pdf and printing out lowercased content
for page in pages:
    normalised = normalise_text(page.page_content)
    print(normalised)
