import hashlib
import re

def hash_sensitive_info(text: str) -> str:
    """Hash sensitive patient identifiers while preserving medical context."""
    
    def _hash(value):
        return hashlib.sha256(value.encode()).hexdigest()[:10]
    
    # Generic patterns only - no hardcoded names
    patterns = [
        # Contextual patterns (preserve labels)
        (r'(Patient name\s+)([^\n]+)', lambda m: m.group(1) + _hash(m.group(2).strip())),
        (r'(NHS number\s+)([^\s]+)', lambda m: m.group(1) + _hash(m.group(2))),
        (r'(Hospital ID\s+)([^\s]+)', lambda m: m.group(1) + _hash(m.group(2))),
        (r'(GP name\s+)([^\n]+)', lambda m: m.group(1) + _hash(m.group(2).strip())),
        
        # All email addresses
        (r'\S+@\S+\.\w+', lambda m: _hash(m.group(0))),
        
        # All phone numbers
        (r'\b\d{3}\s+\d{4}\s+\d{3}\b', lambda m: _hash(m.group(0))),
        (r'\(\d{5}\)\s+\d{6}', lambda m: _hash(m.group(0))),
        
        # Names with titles (Mr, Mrs, Ms, Miss, Dr)
        (r'\b(?:Mr|Mrs|Ms|Miss|Dr)\.\s+[A-Z](?:\.\s+)?[A-Za-z\']+(?:\s+[A-Za-z\']+)*', lambda m: _hash(m.group(0))),
        
        # Professional names (First Last format before job titles)
        (r'\b[A-Z][a-z]+\s+[A-Z][a-z]+(?=\s*,?\s*(?:Community|Hospital|Feeding)\s+(?:dietician|Dietician|nurse|Nurse|Neurologist))', lambda m: _hash(m.group(0))),
        
        # Names in parentheses
        (r'\([A-Z][a-z]+\s+[A-Z][a-z]+\)', lambda m: '(' + _hash(m.group(0)[1:-1]) + ')'),
        
        # Standalone surnames (capitalize words not followed by medical terms)
        (r'\b[A-Z][a-z]{3,}(?=\s*(?:\n|$|,|\(patient\)))', lambda m: _hash(m.group(0))),
        
        # Dear + title + name pattern
        (r'(Dear\s+)((?:Mr|Mrs|Ms|Miss|Dr)\.\s+[A-Za-z\']+)', lambda m: m.group(1) + _hash(m.group(2))),
    ]
    
    # Apply patterns in order
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    
    return text