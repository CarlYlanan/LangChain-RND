import re
import csv

def extract_patient_data(text):
    name = re.search(r"Patient name\s+(.+)", text)
    dob = re.search(r"Date of birth\s+([0-9/]+)", text)
    gender = re.search(r"Gender\s+(\w+)", text)
    email = re.search(r"Patient email\s+address\s+([^\s]+)", text)
    diagnosis = re.search(r"Diagnoses:\s+(.+)", text)

    return {
        "name": name.group(1) if name else "Unknown",
        "dob": dob.group(1) if dob else "Unknown",
        "gender": gender.group(1) if gender else "Unknown",
        "email": email.group(1) if email else "Unknown",
        "diagnosis": diagnosis.group(1) if diagnosis else "Unknown"
    }

# Example extracted text (From sample1 1.pdf)
sample_text = """
Patient name Mr. Thomas  (Tom) Linacre
Date of birth 01/01/1960
Gender Male
Patient email address thomas@linacre.net
Diagnoses: Stroke Problems and issues: Acquired swallowing difficulties
"""

# Extract and store structured data
patient_data = extract_patient_data(sample_text)

# Save to CSV
with open("simple_patient_data.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=patient_data.keys())
    writer.writeheader()
    writer.writerow(patient_data)
