import os
from typing_extensions import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader

# Optional: Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = ""

# Load the PDF document
pdf_loader = PyPDFLoader(r'E:\Git\LangChain_Project\LangChain-RND\sample_documents\sample1.pdf')
documents = pdf_loader.load()

# Print the loaded documents
for i, doc in enumerate(documents):
    print(f"Document {i+1}:")
    print(doc)
    print("\n" + "-"*50 + "\n")

# Define the schema using TypedDict and Annotated
class MedicalKeywordExtraction(TypedDict):
    diagnoses: Annotated[list[str], "Medical diagnoses mentioned in the report"]
    symptoms: Annotated[list[str], "Symptoms or issues the patient is experiencing"]
    treatments: Annotated[list[str], "Treatments, interventions, or medical devices used"]

# Initialize the chat model and wrap it with structured output
llm = ChatOpenAI(temperature=0)
structured_llm = llm.with_structured_output(MedicalKeywordExtraction)

# Apply the structured model to each document
for i, doc in enumerate(documents):
    print(f"Extracting from Document {i+1}...")
    try:
        result = structured_llm.invoke(doc.page_content)
        print(result)
    except Exception as e:
        print(f"Error processing Document {i+1}: {e}")
    print("\n" + "-"*50 + "\n")
