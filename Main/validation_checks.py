import sys
print(sys.executable)

import re
from collections import defaultdict
from langchain_community.document_loaders import PyPDFLoader

# Load PDF
loader = PyPDFLoader("../sample_documents/sample1.pdf")
documents = loader.load()
pages = [doc.page_content for doc in documents]

for i, page in enumerate(pages, start=1):
    print(f"\n--- Page {i} ---\n{page[:500]}...\n")


# Define fields to track
fields = ["Patient name", "Date of birth", "Hospital ID"]
field_matches = defaultdict(list)

for i, text in enumerate(pages):
    for field in fields:
        pattern = rf"{re.escape(field)}[\s:]*([^\n]+)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            # Manually remove trailing unwanted text for 'Date of birth'
            if field.lower() == "date of birth":
                # Remove everything starting from 'Contact type' or any other trailing label
                value = re.split(r"\sContact type|\sGender|\sNHS number", value)[0].strip()
            print(f"Found '{field}' on page {i+1}: {value}")
            field_matches[field].append((i+1, value))


# Check for inconsistencies
for field, values in field_matches.items():
    unique_vals = set(val for _, val in values)
    if len(unique_vals) > 1:
        print(f"\n❗ Inconsistency found in '{field}':")
        for page_num, val in values:
            print(f"  - Page {page_num}: {val}")

