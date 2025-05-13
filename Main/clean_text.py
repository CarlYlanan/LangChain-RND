import re
from langchain.document_loaders import PyPDFLoader

import re

def clean_text(text: str) -> str:
    """
    Gently cleans the text by:
    - Removing unwanted special characters
    - Preserving useful punctuation: . , : ( ) / - @ '
    - Collapsing multiple spaces but keeping newlines
    """
    # Keep common punctuation needed for readability and clinical clarity
    allowed_punctuation = r"[^\w\s\.,:()/@'-]"  # remove everything else

    # Remove unwanted characters
    text = re.sub(allowed_punctuation, '', text)

    # Normalise spacing per line while preserving newlines
    lines = text.splitlines()
    cleaned_lines = [re.sub(r'\s+', ' ', line).strip() for line in lines]

    return '\n'.join(cleaned_lines)
   



# Importing pdfreader to read sample documents
loader1 = PyPDFLoader("sample_documents/sample1.pdf")
pages = loader1.load()

# Loop through all pages within pdf and printing out cleaned text
for i, page in enumerate(pages):
    cleaned = clean_text(page.page_content)
    print(f"\n--- Cleaned Page {i + 1} ---\n")
    print(cleaned)
