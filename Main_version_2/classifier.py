import os
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_community.document_loaders import PyPDFLoader

#Load environment variables (for API keys)
load_dotenv()

#Set up OpenAI model
llm = ChatOpenAI(temperature=0)

#Prompt for classification (structured, semi strucured, or unstructured)
prompt = PromptTemplate.from_template(
    """You are a document classification assistant. Given a clinical paragraph, classify it as one of:

- 'structured': if the text is made up almost entirely of clearly labeled fields or values in "key value" format.
- 'semi-structured': if the text contains some formatting or lists, but also includes prose or explanations.
- 'unstructured': if it is free-form narrative, patient observations, or notes with little to no formatting.

Only reply with: structured, semi-structured, or unstructured.

Examples:
---
Text:
"Patient Name: Tom Linacre
NHS number: 789123456
Contact type: First appointment "
-> structured

Text:
"Patient presents with recurrent UTI symptoms. Prior labs suggest ongoing infection..."
-> unstructured

Text:
"History: Chronic kidney pain. Treatment: Reviewed CT scans. Advised surgery."
-> semi-structured
---
Text:
{text}
→"""
)

classifier_chain = prompt | llm

def classify_chunk(chunk: str, verbose=False) -> str:
    """Use OpenAI to classify a paragraph/chunk of text."""
    response = classifier_chain.invoke({"text": chunk})
    label = response.content.strip().lower()

    if verbose:
        print(f"\nClassified as: {label}\n Preview: {chunk[:150]}...\n")

    return label


def split_into_chunks(text: str, min_words=1) -> list:
    """Split full document into paragraph-like chunks using blank lines."""
    raw_chunks = re.split(r"\n\s*\n", text)
    return [chunk.strip() for chunk in raw_chunks if len(chunk.strip().split()) >= min_words]


def clean_structured_chunk(chunk):
    lines = chunk.splitlines()
    cleaned_lines = []
    skip_next = False

    for i in range(len(lines)):
        if skip_next:
            skip_next = False
            continue

        current = lines[i].strip()
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""

        #Merge if current line seems like a label (ends in ":" or contains "date of", etc.)
        if (
            current.endswith(":")
            or re.match(r"(date|patient|gp|hospital|contact|number|email|address)\s", current.lower())
        ) and next_line and not next_line.endswith("."):
            merged = f"{current} {next_line}"
            cleaned_lines.append(merged)
            skip_next = True
        else:
            cleaned_lines.append(current)

    return "\n".join(cleaned_lines)


def split_document_sections_by_chunks(text: str):
    structured, semi_structured, unstructured = [], [], []

    chunks = split_into_chunks(text)
    for chunk in chunks:
        label = classify_chunk(chunk)
        #print("CHUNK START >>>")
        #print(chunk)
        #print("<<< CHUNK END\n")

        if "structured" in label and "semi" not in label and "un" not in label:
            structured.append(clean_structured_chunk(chunk))
        elif "semi" in label:
            semi_structured.append(chunk)
        elif "unstructured" in label or "free text" in label:
            unstructured.append(chunk)
        else:
            unstructured.append(chunk)

    return {
        "structured": structured,
        "semi_structured": semi_structured,
        "unstructured": unstructured
    }

def run_classification_pipeline(text: str):
    """
    Takes text and runs classification.
    """
    sections = split_document_sections_by_chunks(text)

    print("\n======= STRUCTURED =======\n")
    print("\n\n".join(sections["structured"]))

    print("\n======= SEMI-STRUCTURED =======\n")
    print("\n\n".join(sections["semi_structured"]))

    print("\n======= UNSTRUCTURED =======\n")
    print("\n\n".join(sections["unstructured"]))

    print("\n=== Summary ===")
    print(f"Structured chunks: {len(sections['structured'])}")
    print(f"Semi-structured chunks: {len(sections['semi_structured'])}")
    print(f"Unstructured chunks: {len(sections['unstructured'])}")

    return sections


def get_semi_and_unstructured(text: str):
    """
    Returns semi-structured and unstructured chunks,
    plus any structured chunks that mention DOB (which are important for triage).

    Includes optional preview code that can be enabled for debugging or client review.
    """
    sections = split_document_sections_by_chunks(text)

    semi = sections["semi_structured"]
    unstructured = sections["unstructured"]

    '''

    # Print full chunks for client validation, uncomment if needed
    
    print("\n=== FULL EXTRACTED TEXT ===")

    
    #if dob_lines:
    #   print("\n--- Structured with DOB ---")
     #   for i, line in enumerate(dob_lines, 1):
      #      print(f"\n[{i}] {line}")
    

    if semi:
        print("\n--- Semi-Structured ---")
        for i, chunk in enumerate(semi, 1):
            print(f"\n[{i}] {chunk}")

    if unstructured:
        print("\n--- Unstructured ---")
        for i, chunk in enumerate(unstructured, 1):
            print(f"\n[{i}] {chunk}")
    
    '''
    return semi + unstructured
    
