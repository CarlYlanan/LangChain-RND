triage_rules ="""
Urology Referral Grading Matrix – New Zealand Context

This grading matrix outlines clinical indicators and triaging criteria for urology referrals across New Zealand, aligned with standard regional practices. It is designed to support automation of triage using AI/NLP tools by defining precise indicators, language patterns, and prioritisation rules.

Referral Categories and Timeframes

Referral Category
Examples / Clinical Indicators
Grading
Target Timeframe
Notes

Suspected Cancer
Macroscopic haematuria, Raised PSA + abnormal DRE, Testicular mass, Penile lesion
Priority 1
Seen within 2 weeks
Red flag symptoms – suspected urological malignancy

Significant Symptoms / Risk of Harm
Recurrent urinary retention, Obstructive uropathy, Ureteric stone, Severe LUTS
Priority 2
Seen within 4–6 weeks
Risk of deterioration or hospitalisation

Moderate Symptoms / Non-Urgent
Non-visible haematuria, Moderate LUTS, Erectile dysfunction, Stable PSA rise
Priority 3
Seen within 3–4 months
May benefit from specialist input but not urgent

Stable / Routine Review
Longstanding incontinence, Vasectomy referral, Stable renal cyst
Priority 4
Seen within 6–12 months
Routine or elective; safe to defer

Return to GP / Not Accepted
Incomplete referral, Managed in primary care, Not in urology scope
N/A
N/A
Referral returned with guidance

Detailed Clinical Indicators for Automation

Priority 1: Suspected Cancer
• Macroscopic haematuria
  Trigger Terms: "visible blood in urine", "gross haematuria", "red urine"
  Clinical Context: Requires urgent cystoscopy and imaging, especially over age 45.
• Raised PSA + abnormal DRE
  Trigger Terms: "elevated PSA", "abnormal prostate exam", "nodular prostate"
  Clinical Context: Suspicion of prostate cancer.
• Testicular mass
  Trigger Terms: "lump in testicle", "testicular swelling", "scrotal mass"
  Clinical Context: Urgent scrotal ultrasound to rule out malignancy.
• Penile lesion
  Trigger Terms: "penile ulcer", "non-healing sore on penis"
  Clinical Context: Suspicion of penile cancer, needs urgent biopsy.

Priority 2: Significant Symptoms / Risk of Harm
• Recurrent urinary retention
  Trigger Terms: "urinary retention", "TOWC", "catheter dependent"
  Clinical Context: Multiple episodes requiring specialist input.
• Obstructive uropathy
  Trigger Terms: "hydronephrosis", "eGFR decline", "bilateral obstruction"
  Clinical Context: Possible bilateral obstruction or solitary kidney.
• Ureteric stone
  Trigger Terms: "stone in ureter", "ureteric colic"
  Clinical Context: Painful, >5mm, or not resolving.
• Severe LUTS
  Trigger Terms: "nocturia x5", "urge incontinence", "not responding to tamsulosin"
  Clinical Context: Severe impact on quality of life.

Priority 3: Moderate Symptoms / Non-Urgent
• Non-visible haematuria
  Trigger Terms: "microscopic haematuria", "RBCs on dipstick"
  Clinical Context: Persistent; requires investigation esp. if over 60.
• Moderate LUTS
  Trigger Terms: "weak stream", "incomplete emptying"
  Clinical Context: Stable and manageable with medical treatment.
• Erectile dysfunction
  Trigger Terms: "ED", "loss of erection"
  Clinical Context: Not responding to primary care treatment.
• Stable PSA rise
  Trigger Terms: "PSA velocity", "rising PSA"
  Clinical Context: Within tolerable limits without suspicious DRE findings.

Priority 4: Stable / Routine Review
• Longstanding incontinence
  Trigger Terms: "chronic leakage", "stress incontinence"
  Clinical Context: Stable; suitable for conservative management.
• Vasectomy
  Trigger Terms: "vasectomy request", "sterilisation"
  Clinical Context: Elective; no urgency.
• Stable renal cyst
  Trigger Terms: "Bosniak 1 cyst", "incidental renal cyst"
  Clinical Context: No concern for malignancy.

Not Accepted / Return to GP
• Incomplete referral
  Trigger Terms: "missing PSA", "no clinical details"
  Clinical Context: Request clarification or additional info.
• Managed in primary care
  Trigger Terms: "mild LUTS", "early ED"
  Clinical Context: Advice back to GP.
• Out of scope
  Trigger Terms: "not urology", "refer to another specialty"
  Clinical Context: Redirect referral appropriately.
"""
