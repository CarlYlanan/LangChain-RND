from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from med_models import Patient, NoteToTriage, PatientResult, Rule

def database_update(data_list) -> None:
    """
    updating the database with new patient data, notes, and triage results.

    arguments:
        data_list (list of dict): Each dict contains keys like
          - patient_info: dict with nhs_number, name, dob, gender, etc.
          - note_text: raw referral or clinical note text
          - triage_results: list of dicts with rule_id, matched_trigger_terms, negation_detected, confidence_score

    For each item:
        - Upsert patient by nhs_number
        - Insert a new note linked to patient
        - Insert triage results linked to patient, note, and rule
    """

    try:
        engine = create_engine('postgresql://postgres@localhost/postgres')
        Session = sessionmaker(bind=engine)
        session = Session()

        for item in data_list:
            p_info = item['patient_info']
            note_text = item['note_text']
            triage_results = item.get('triage_results', [])

            # 1. Upsert Patient
            patient = session.query(Patient).filter_by(nhs_number=p_info['nhs_number']).first()
            if not patient:
                patient = Patient(**p_info)
                session.add(patient)
                session.flush()  # flush to get patient_id
                print(f"[INFO] Inserted new patient: {patient.nhs_number}")
            else:
                # Update patient fields if needed
                updated = False
                for key, val in p_info.items():
                    if getattr(patient, key) != val:
                        setattr(patient, key, val)
                        updated = True
                if updated:
                    print(f"[INFO] Updated patient: {patient.nhs_number}")

            # 2. Insert Note
            note = NoteToTriage(patient_id=patient.patient_id, text=note_text)
            session.add(note)
            session.flush()  # get note_id
            print(f"[INFO] Inserted note for patient {patient.nhs_number} (note_id={note.note_id})")

            # 3. Insert Triage Results
            for triage in triage_results:
                # Validate rule exists
                rule = session.query(Rule).filter_by(rule_id=triage['rule_id']).first()
                if not rule:
                    print(f"[WARNING] Rule ID {triage['rule_id']} not found, skipping triage result.")
                    continue

                result = PatientResult(
                    patient_id=patient.patient_id,
                    note_id=note.note_id,
                    rule_id=rule.rule_id,
                    matched_trigger_terms=triage.get('matched_trigger_terms'),
                    negation_detected=triage.get('negation_detected', False),
                    confidence_score=triage.get('confidence_score', 0.0),
                    triaged_at=datetime.utcnow()
                )
                session.add(result)
                print(f"[INFO] Inserted triage result for patient {patient.nhs_number} with rule {rule.rule_id}")

        session.commit()
        print("[SUMMARY] Database update complete.")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"[ERROR] Database error: {e}")

if __name__ == "__main__":
    database_update()

