triage_rules = {
    "Priority 1": {
        "label": "Suspected Cancer",
        "target_timeframe": "Seen within 2 weeks",
        "examples": [
            "Macroscopic haematuria",
            "Raised PSA + abnormal DRE",
            "Testicular mass",
            "Penile lesion"
        ],
        "trigger_terms": [
            "visible blood in urine", "gross haematuria", "red urine",
            "elevated PSA", "abnormal prostate exam", "nodular prostate",
            "lump in testicle", "testicular swelling", "scrotal mass",
            "penile ulcer", "non-healing sore on penis"
        ],
        "rationale": "Red flag symptoms – suspected urological malignancy"
    },

    "Priority 2": {
        "label": "Significant Symptoms / Risk of Harm",
        "target_timeframe": "Seen within 4–6 weeks",
        "examples": [
            "Recurrent urinary retention",
            "Obstructive uropathy",
            "Ureteric stone",
            "Severe LUTS"
        ],
        "trigger_terms": [
            "urinary retention", "TOWC", "catheter dependent",
            "hydronephrosis", "eGFR decline", "bilateral obstruction",
            "stone in ureter", "ureteric colic",
            "nocturia x5", "urge incontinence", "not responding to tamsulosin"
        ],
        "rationale": "Risk of deterioration or hospitalisation"
    },

    "Priority 3": {
        "label": "Moderate Symptoms / Non-Urgent",
        "target_timeframe": "Seen within 3–4 months",
        "examples": [
            "Non-visible haematuria",
            "Moderate LUTS",
            "Erectile dysfunction",
            "Stable PSA rise"
        ],
        "trigger_terms": [
            "microscopic haematuria", "RBCs on dipstick",
            "weak stream", "incomplete emptying",
            "ED", "loss of erection",
            "PSA velocity", "rising PSA"
        ],
        "rationale": "May benefit from specialist input but not urgent"
    },

    "Priority 4": {
        "label": "Stable / Routine Review",
        "target_timeframe": "Seen within 6–12 months",
        "examples": [
            "Longstanding incontinence",
            "Vasectomy referral",
            "Stable renal cyst"
        ],
        "trigger_terms": [
            "chronic leakage", "stress incontinence",
            "vasectomy request", "sterilisation",
            "Bosniak 1 cyst", "incidental renal cyst"
        ],
        "rationale": "Routine or elective; safe to defer"
    },

    "Not Accepted": {
        "label": "Return to GP",
        "target_timeframe": "N/A",
        "examples": [
            "Incomplete referral",
            "Managed in primary care",
            "Not in urology scope"
        ],
        "trigger_terms": [
            "missing PSA", "no clinical details",
            "mild LUTS", "early ED",
            "not urology", "refer to another specialty"
        ],
        "rationale": "Referral returned with guidance"
    }
}