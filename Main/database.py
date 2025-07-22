from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.inspection import inspect
from datetime import datetime
from med_models import MedResult, RecentUpdate

def database_update() -> None:
    """
    Synchronizes all data from recent_update table into med_results table in the local PostgreSQL database.

    This function:
    - Retrieves all rows from recent_update.
    - For each row, finds the matching med_results row by nhs_number.
    - Compares each column one by one.
    - Updates med_results columns where values differ and recent_update value is not None.
    - Tracks and reports number of updated and skipped records.
    - Commits changes in a single transaction at the end.
    """
    try:
        engine = create_engine('postgresql://postgres@localhost/postgres')
        Session = sessionmaker(bind=engine)
        session = Session()

        records_updated = 0
        records_skipped = 0

        recent_rows = session.query(RecentUpdate).all()
        print(f"[INFO] Retrieved {len(recent_rows)} rows from recent_update.")

        columns_to_check = [
            column.key for column in inspect(RecentUpdate).mapper.column_attrs
            if column.key != "id"
        ]

        for recent_row in recent_rows:
            nhs = recent_row.nhs_number

            existing_row = session.query(MedResult).filter_by(nhs_number=nhs).first()

            if existing_row is None:
                print(f"[SKIP] No matching med_results record for NHS Number: {nhs}. Skipping update.")
                records_skipped += 1
                continue

            row_needs_update = False
            print(f"[PROCESS] Checking updates for NHS Number: {nhs}.")

            for column in columns_to_check:
                recent_value = getattr(recent_row, column)
                existing_value = getattr(existing_row, column)

                if recent_value is not None:
                    if existing_value != recent_value:
                        print(f"  - Column '{column}': updating from '{existing_value}' to '{recent_value}'.")
                        setattr(existing_row, column, recent_value)
                        row_needs_update = True
                    else:
                        print(f"  - Column '{column}': no change (value: '{existing_value}').")
                else:
                    print(f"  - Column '{column}': recent_update value is None, skipping update.")

            if row_needs_update:
                existing_row.updated_at = datetime.utcnow()
                records_updated += 1
                print(f"[UPDATE] NHS Number {nhs} record updated.")
            else:
                print(f"[NO UPDATE] NHS Number {nhs} record unchanged.")

        session.commit()

        print(f"[SUMMARY] Synchronization complete.")
        print(f"  - Total records processed: {len(recent_rows)}")
        print(f"  - Records updated: {records_updated}")
        print(f"  - Records skipped (no match): {records_skipped}")

        session.close()

    except SQLAlchemyError as error:
        print(f"[ERROR] Database error occurred: {error}")

if __name__ == "__main__":
    database_update()
