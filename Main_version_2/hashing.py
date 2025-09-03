import hashlib
import re
import random
import string
from pathlib import Path

# Load first and last names once
FIRST_NAMES_FILE = Path("name_replacements/first_names.txt")
LAST_NAMES_FILE = Path("name_replacements/last_names.txt")

with FIRST_NAMES_FILE.open("r", encoding="utf-8") as f:
    FIRST_NAMES = [line.strip() for line in f if line.strip()]
with LAST_NAMES_FILE.open("r", encoding="utf-8") as f:
    LAST_NAMES = [line.strip() for line in f if line.strip()]

# Global sets to track used combinations across all function calls
USED_FULL_NAMES = set()
USED_PHONE_NUMBERS = set()
USED_NHI_NUMBERS = set()

def hash_sensitive_info(text: str) -> str:
    """
    Hash sensitive patient identifiers while preserving medical context.
    Generates fake personal information using external name files.
    Ensures all generated names and IDs are unique without duplication.
    """
    
    def _hash(value):
        return hashlib.sha256(value.encode()).hexdigest()[:10]
    
    def generate_unique_full_name(max_attempts=1000):
        """Generate a unique full name combination"""
        for _ in range(max_attempts):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            full_name = f"{first_name} {last_name}"
            
            if full_name not in USED_FULL_NAMES:
                USED_FULL_NAMES.add(full_name)
                return full_name
        
        # If we can't find a unique combination after max_attempts, 
        # add a number suffix to ensure uniqueness
        base_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        counter = 1
        while f"{base_name}_{counter}" in USED_FULL_NAMES:
            counter += 1
        
        unique_name = f"{base_name}_{counter}"
        USED_FULL_NAMES.add(unique_name)
        return unique_name
    
    def generate_unique_phone(max_attempts=1000):
        """Generate a unique 10-digit phone number"""
        for _ in range(max_attempts):
            phone = "".join([str(random.randint(0, 9)) for _ in range(10)])
            
            if phone not in USED_PHONE_NUMBERS:
                USED_PHONE_NUMBERS.add(phone)
                return phone
        
        # Fallback: if somehow we can't generate unique after max_attempts
        # This is extremely unlikely with 10 billion possible combinations
        counter = 1
        base_phone = "".join([str(random.randint(0, 9)) for _ in range(8)])
        while f"{base_phone}{counter:02d}" in USED_PHONE_NUMBERS:
            counter += 1
        
        unique_phone = f"{base_phone}{counter:02d}"
        USED_PHONE_NUMBERS.add(unique_phone)
        return unique_phone
    
    def generate_unique_nhi(max_attempts=1000):
        """Generate a unique NHI number (2 letters + 5 numbers)"""
        for _ in range(max_attempts):
            letters = "".join(random.choices(string.ascii_uppercase, k=2))
            numbers = "".join([str(random.randint(0, 9)) for _ in range(5)])
            nhi = letters + numbers
            
            if nhi not in USED_NHI_NUMBERS:
                USED_NHI_NUMBERS.add(nhi)
                return nhi
        
        # Fallback: systematic generation if random fails
        counter = 1
        base_letters = "".join(random.choices(string.ascii_uppercase, k=2))
        while f"{base_letters}{counter:05d}" in USED_NHI_NUMBERS:
            counter += 1
        
        unique_nhi = f"{base_letters}{counter:05d}"
        USED_NHI_NUMBERS.add(unique_nhi)
        return unique_nhi
    
    # Dictionary to store mappings for this processing session
    mappings = {}
    
    def replace_with_fake(pattern_type, original_value):
        """Replace original value with unique fake data"""
        if original_value in mappings:
            return mappings[original_value]
        
        if pattern_type == "phone":
            fake_value = generate_unique_phone()
        elif pattern_type == "nhi":
            fake_value = generate_unique_nhi()
        elif pattern_type == "name":
            fake_value = generate_unique_full_name()
        else:
            fake_value = _hash(original_value)
        
        mappings[original_value] = fake_value
        return fake_value
    
    # Medical field terms that should NOT be replaced
    medical_exclusions = {
        'Date', 'Birth', 'Gender', 'Male', 'Female', 'Contact', 'Type', 'Consultation', 'Method', 
        'Face', 'Seen', 'Outcome', 'Patient', 'Attendance', 'Practice', 'Details', 'Identifier',
        'Address', 'Email', 'Telephone', 'Number', 'Appointment', 'Follow', 'First', 'Referral',
        'Emergency', 'Admission', 'Department', 'Hospital', 'Centre', 'Clinic', 'General',
        'Practitioner', 'Consultant', 'Urologist', 'Dietician', 'Neurologist', 'Community',
        'Feeding', 'Nurse', 'Diagnoses', 'History', 'Examinations', 'Investigations', 'Clinical',
        'Summary', 'Allergies', 'Adverse', 'Reactions', 'Changes', 'Medications', 'Medical',
        'Devices', 'Actions', 'Healthcare', 'Professionals', 'Information', 'Advice', 'Given',
        'Yours', 'Sincerely', 'Distribution', 'List', 'Time', 'Weight', 'Height', 'Blood',
        'Pressure', 'Temp', 'Temperature', 'Abdominal', 'Exam', 'Examination', 'Digital',
        'Rectal', 'Prostate', 'Urine', 'Culture', 'Bloods', 'Renal', 'Function', 'Urinalysis',
        'Microscopic', 'Haematuria', 'Lower', 'Urinary', 'Tract', 'Symptoms', 'LUTS', 'Therapy',
        'Treatment', 'Surgery', 'Surgical', 'Intervention', 'Monitoring', 'Surveillance'
    }
    
    def is_medical_term(text):
        """Check if text contains medical field terms that shouldn't be replaced"""
        words = text.split()
        return any(word.strip('.,():') in medical_exclusions for word in words)
    
    def safe_name_replace(match_obj, pattern_type):
        """Only replace if it's not a medical term"""
        matched_text = match_obj.group(0)
        if is_medical_term(matched_text):
            return matched_text  # Don't replace medical terms
        return replace_with_fake(pattern_type, matched_text)

    # More precise patterns with medical term exclusions
    patterns = [
        # Specific contextual patterns (most reliable)
        (r"(Patient name\s*:?\s*)([^\n]+)",
         lambda m: m.group(1) + replace_with_fake("name", m.group(2).strip())),
        (r"(GP name\s*:?\s*)([^\n]+)",
         lambda m: m.group(1) + replace_with_fake("name", m.group(2).strip())),
        (r"(Seen by\s+)([^\n,]+?)(?=,|\n|$)",
         lambda m: m.group(1) + replace_with_fake("name", m.group(2).strip())),
        
        # NHS and Hospital IDs
        (r"(NHS number\s*:?\s*)([A-Z]{2}\d{5})",
         lambda m: m.group(1) + replace_with_fake("nhi", m.group(2))),
        (r"\b[A-Z]{2}\d{5}\b",
         lambda m: replace_with_fake("nhi", m.group(0))),
        (r"(Hospital ID\s*:?\s*)([^\s\n]+)",
         lambda m: m.group(1) + _hash(m.group(2))),
        
        # Email addresses and phone numbers
        (r"\S+@\S+\.\w+", lambda m: _hash(m.group(0))),
        (r"\b\d{3}\s*\d{3}\s*\d{4}\b",
         lambda m: replace_with_fake("phone", re.sub(r"\s", "", m.group(0)))),
        (r"\b\d{10}\b",
         lambda m: replace_with_fake("phone", m.group(0))),
        (r"\(\d{3}\)\s*\d{3}-?\d{4}",
         lambda m: replace_with_fake("phone", re.sub(r"[^\d]", "", m.group(0)))),
        
        # Names with titles (most reliable name pattern)
        (r"\b(?:Mr|Mrs|Ms|Miss|Dr)\.\s*[A-Z](?:\.\s*)?[A-Za-z']+(?:\s+[A-Za-z']+)*",
         lambda m: replace_with_fake("name", m.group(0))),
        
        # Names in specific contexts (more targeted)
        (r"\b[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}(?=\s*,?\s*(?:Community|Hospital|Feeding)\s+(?:dietician|Dietician|nurse|Nurse|Neurologist))",
         lambda m: replace_with_fake("name", m.group(0))),
        
        # Names in parentheses
        (r"\([A-Z][a-z]{3,}\s+[A-Z][a-z]{3,}\)",
         lambda m: "(" + replace_with_fake("name", m.group(0)[1:-1]) + ")"),
        
        # "Dear" + name pattern
        (r"(Dear\s+)((?:Mr|Mrs|Ms|Miss|Dr)\.\s*[A-Za-z']+)",
         lambda m: m.group(1) + replace_with_fake("name", m.group(2))),
        
        # RE: pattern (common in medical letters)
        (r"(RE:\s*)([A-Z][a-z]{2,}\s+[A-Z][a-z]{2,})",
         lambda m: m.group(1) + replace_with_fake("name", m.group(2)) if not is_medical_term(m.group(2)) else m.group(0)),
        
        # Signature lines (names at end of documents)
        (r"(Yours sincerely,?\s*\n?\s*)([A-Z][a-z]{2,}\s+[A-Z][a-z]{2,})",
         lambda m: m.group(1) + replace_with_fake("name", m.group(2)) if not is_medical_term(m.group(2)) else m.group(0)),
        
        # Only very specific standalone name patterns (last resort, most restrictive)
        (r"\b[A-Z][a-z]{3,}\s+[A-Z][a-z]{3,}(?=\s*(?:\n|$|,|\(patient\)|\s+\(patient\)))",
         lambda m: safe_name_replace(m, "name")),
    ]
    
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    
    return text

def get_usage_statistics():
    """Get current usage statistics for generated fake data"""
    return {
        "used_full_names": len(USED_FULL_NAMES),
        "used_phone_numbers": len(USED_PHONE_NUMBERS),
        "used_nhi_numbers": len(USED_NHI_NUMBERS),
        "available_name_combinations": len(FIRST_NAMES) * len(LAST_NAMES) - len(USED_FULL_NAMES),
        "available_phone_numbers": 10**10 - len(USED_PHONE_NUMBERS),
        "available_nhi_numbers": 26**2 * 10**5 - len(USED_NHI_NUMBERS)
    }

def reset_usage_tracking():
    """Reset all usage tracking - useful for testing or starting fresh"""
    global USED_FULL_NAMES, USED_PHONE_NUMBERS, USED_NHI_NUMBERS
    USED_FULL_NAMES.clear()
    USED_PHONE_NUMBERS.clear()
    USED_NHI_NUMBERS.clear()

def export_used_combinations(filename="used_combinations.txt"):
    """Export all used combinations to a file for review"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== USED FULL NAMES ===\n")
        for name in sorted(USED_FULL_NAMES):
            f.write(f"{name}\n")
        
        f.write("\n=== USED PHONE NUMBERS ===\n")
        for phone in sorted(USED_PHONE_NUMBERS):
            f.write(f"{phone}\n")
        
        f.write("\n=== USED NHI NUMBERS ===\n")
        for nhi in sorted(USED_NHI_NUMBERS):
            f.write(f"{nhi}\n")
    
    print(f"Used combinations exported to {filename}")