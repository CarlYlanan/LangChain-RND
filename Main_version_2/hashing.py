import re
import random
import string
import os
import json
from typing import Tuple, Dict, Set
from medical_exclusion_terms import medical_exclusions

# ----------------- Paths & Constants -----------------
_FIRST_NAMES_PATH = './name_replacements/first_names.txt'
_LAST_NAMES_PATH = './name_replacements/last_names.txt'
_USED_NAMES_PATH = './name_replacements/used_names.json'
_FIXED_EMAIL = 'totallyrealnotfakeemailaddress@emailingemail.com'

# ----------------- Regex Patterns -----------------
_title_regex = r'(Mr|Mrs|Ms|Miss|Dr|Prof|Professor|Sir|Mx)\.?'
_full_name_regex = re.compile(r'\b([A-Z][a-zA-Z\-]+)\s+([A-Z][a-zA-Z\-]+)\b')
_title_last_regex = re.compile(r'\b' + _title_regex + r'\.?\s+([A-Z][a-zA-Z\-]+)\b')
_nhi_regex = re.compile(r'\b([A-Za-z]{2}\d{5})\b')
_email_regex = re.compile(r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b')
_phone_candidate_regex = re.compile(
    r'(?<!\w)(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?){1,4}\d{3,4}(?!\w)'
)

# ----------------- Exclusions & Context -----------------
_exclusion_set: Set[str] = {term.lower().strip('.,:;()[]{}"\'') for term in medical_exclusions}

_medical_context_patterns = [
    r'\b(diagnosis|condition|disease|syndrome|disorder|infection|cancer|tumor|malignancy)\b',
    r'\b(hospital|clinic|medical|health|department|center|institute|university)\b',
    r'\b(street|road|avenue|lane|drive|boulevard|way|place|court|circle)\b',
    r'\b(north|south|east|west|central|main|first|second|third)\b',
    r'\b(examination|test|result|finding|report|study|scan|x-ray|mri|ct)\b',
    r'\b(medication|drug|treatment|therapy|procedure|surgery|operation)\b',
]
_medical_context_regex = re.compile('|'.join(_medical_context_patterns), re.IGNORECASE)

_common_non_names = {
    'january','february','march','april','may','june','july','august','september','october','november','december',
    'monday','tuesday','wednesday','thursday','friday','saturday','sunday',
    'morning','afternoon','evening','night','today','tomorrow','yesterday',
    'acute','chronic','severe','mild','moderate','benign','malignant',
    'primary','secondary','tertiary','bilateral','unilateral','anterior','posterior','superior','inferior',
    'medial','lateral','proximal','distal','left','right','upper','lower','inner','outer','deep','superficial',
    'normal','abnormal','positive','negative','elevated','decreased','increased','stable','improved','worsened','resolved','pending'
}

# ----------------- Helper Functions -----------------
def _load_replacements(path: str) -> list:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ['Alex','Sam','Jordan','Taylor','Casey','Riley','Jamie','Morgan'] if 'first_names' in path else ['Smith','Brown','Taylor','Wilson','Johnson','Lee','Martin','Clark']

def _random_letter_sequence(n: int) -> str:
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(n))

def _random_digits(n: int) -> str:
    return ''.join(random.choice(string.digits) for _ in range(n))

def _preserve_separators_replace_digits(orig: str) -> str:
    return ''.join(random.choice(string.digits) if ch.isdigit() else ch for ch in orig)

def _contains_excluded_term(phrase: str) -> bool:
    """Check if any individual word in the phrase is in the exclusion set"""
    words = phrase.lower().strip('.,:;()[]{}"\'').split()
    for word in words:
        clean_word = word.strip('.,:;()[]{}"\'')
        if clean_word in _exclusion_set or clean_word in _common_non_names:
            return True
    return False

def _has_medical_context(text: str, start_pos: int, end_pos: int, window_size: int = 100) -> bool:
    text_start = max(0, start_pos - window_size)
    text_end = min(len(text), end_pos + window_size)
    return bool(_medical_context_regex.search(text[text_start:text_end]))

def _looks_like_name_pair(first: str, last: str) -> bool:
    # Check if either word individually is an excluded term
    if _contains_excluded_term(first) or _contains_excluded_term(last):
        return False
    
    if len(first)<2 or len(first)>20 or len(last)<2 or len(last)>20: return False
    for pattern in [r'^\d+$', r'^[A-Z]{2,}$', r'[0-9]', r'[^a-zA-Z\-\' ]']:
        if re.search(pattern, first) or re.search(pattern, last): return False
    return True

def _looks_like_single_name(word: str) -> bool:
    if _contains_excluded_term(word): return False
    if len(word)<2 or len(word)>20: return False
    if re.search(r'^\d+$|^[A-Z]{2,}$|[0-9]|[^a-zA-Z\-\' ]', word): return False
    return True

def _title_case_like(orig: str, new: str) -> str:
    if orig.isupper(): return new.upper()
    if orig.islower(): return new.lower()
    return new.title()

# ----------------- Main Function -----------------
def hash_sensitive_info(text: str, file_name: str = "unknown_file") -> str:
    random.seed()
    first_pool = _load_replacements(_FIRST_NAMES_PATH)
    last_pool = _load_replacements(_LAST_NAMES_PATH)

    os.makedirs(os.path.dirname(_USED_NAMES_PATH), exist_ok=True)

    # Load existing JSON or create empty
    if os.path.exists(_USED_NAMES_PATH):
        with open(_USED_NAMES_PATH,'r',encoding='utf-8') as f:
            try: used = json.load(f)
            except json.JSONDecodeError: used = {}
    else:
        used = {}

    # Ensure all sub-maps exist
    used.setdefault("fullnames", {})
    used.setdefault("nhis", {})
    used.setdefault("phones", {})

    fullname_map: Dict[str, Tuple[str,str]] = {}
    last_map: Dict[str,str] = {}

    # ----------------- Full Names -----------------
    for m in _full_name_regex.finditer(text):
        orig_first, orig_last = m.group(1), m.group(2)
        orig_full = f'{orig_first} {orig_last}'
        if not _looks_like_name_pair(orig_first, orig_last): continue
        if _has_medical_context(text, m.start(), m.end()): continue

        if orig_full in used["fullnames"]:
            fake_first, fake_last = used["fullnames"][orig_full]["fake"].split(' ',1)
        else:
            fake_first, fake_last = random.choice(first_pool), random.choice(last_pool)
            used["fullnames"][orig_full] = {"fake": f"{fake_first} {fake_last}", "file": file_name}
        fullname_map[orig_full] = (fake_first, fake_last)
        if orig_last not in last_map: last_map[orig_last] = fake_last

    # ----------------- Title + Last Names -----------------
    for m in _title_last_regex.finditer(text):
        last = m.group(2)
        if not _looks_like_single_name(last): continue
        if _has_medical_context(text, m.start(), m.end()): continue

        # Create a temporary full name for consistency (using "Dr" + last format to avoid "Title")
        temp_full = f"Dr {last}"
        if temp_full in used["fullnames"]:
            _, fake_last = used["fullnames"][temp_full]["fake"].split(' ', 1)
        else:
            fake_last = random.choice(last_pool)
            used["fullnames"][temp_full] = {"fake": f"Dr {fake_last}", "file": file_name}
        
        if last not in last_map: 
            last_map[last] = fake_last

    # ----------------- Replace Emails -----------------
    text = _email_regex.sub(_FIXED_EMAIL, text)

    # ----------------- Replace NHIs -----------------
    def nhi_replacer(match):
        orig = match.group(1)
        if orig in used["nhis"]:
            return used["nhis"][orig]["fake"]
        repl = _random_letter_sequence(2) + _random_digits(5)
        used["nhis"][orig] = {"fake": repl, "file": file_name}
        return repl
    text = _nhi_regex.sub(nhi_replacer, text)

    # ----------------- Replace Phones -----------------
    def phone_replacer(match):
        s = match.group(0)
        digits = ''.join(ch for ch in s if ch.isdigit())
        if len(digits)<7: return s
        if s in used["phones"]:
            return used["phones"][s]["fake"]
        repl = _preserve_separators_replace_digits(s)
        used["phones"][s] = {"fake": repl, "file": file_name}
        return repl
    text = _phone_candidate_regex.sub(phone_replacer, text)

    # ----------------- Replace Full Names -----------------
    def replace_fullnames(orig_text: str) -> str:
        def _full_repl(m):
            orig_first, orig_last = m.group(1), m.group(2)
            orig_full = f'{orig_first} {orig_last}'
            if orig_full not in fullname_map: return m.group(0)
            fake_first, fake_last = fullname_map[orig_full]
            return f'{_title_case_like(orig_first,fake_first)} {_title_case_like(orig_last,fake_last)}'
        return _full_name_regex.sub(_full_repl, orig_text)
    text = replace_fullnames(text)

    # ----------------- Replace Title + Last -----------------
    def title_last_replacer(m):
        orig_last = m.group(2)
        if not _looks_like_single_name(orig_last): return m.group(0)
        fake_last = last_map.get(orig_last, orig_last)
        if fake_last == orig_last: return m.group(0)
        return m.group(0).replace(orig_last,_title_case_like(orig_last,fake_last))
    text = _title_last_regex.sub(title_last_replacer,text)

    # ----------------- Replace Lone Last Names -----------------
    if last_map:
        last_keys = sorted(last_map.keys(), key=lambda x:-len(x))
        pattern = r'\b('+'|'.join(re.escape(k) for k in last_keys)+r')\b'
        last_any_re = re.compile(pattern)
        def last_only_repl(m):
            orig_last = m.group(1)
            if not _looks_like_single_name(orig_last): return orig_last
            if _has_medical_context(text,m.start(),m.end(),window_size=50): return orig_last
            fake_last = last_map.get(orig_last, orig_last)
            if fake_last==orig_last: return orig_last
            return _title_case_like(orig_last,fake_last)
        text = last_any_re.sub(last_only_repl,text)

    # ----------------- Save JSON -----------------
    with open(_USED_NAMES_PATH,'w',encoding='utf-8') as f:
        json.dump(used,f,indent=2)

    return text