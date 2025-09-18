import os
import re
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Loading information from .env file
load_dotenv()

def ai_output_info(ai_output: str):
    
    #Removing disclaimer from rationale
    disclaimer_remove = ai_output.split("Disclaimer", 1)[0].strip()

    # Split response into lines
    lines = disclaimer_remove.splitlines()

    triage_result = "Unknown"

    #Look for first Priority X or Not Accepted with value 1
    for line in lines:
        line = line.strip()
        match = re.match(r"(Priority\s*[1-4]|Not Accepted):\s*1\b", line, re.IGNORECASE)
        if match:
            triage_result = match.group(1)
            last_priority_idx = lines.index(line)  # for rationale extraction
            break
    else:
        # If none are 1, fallback to Not Accepted or first Priority line
        for line in lines:
            line = line.strip()
            match = re.match(r"(Priority\s*[1-4]|Not Accepted):", line, re.IGNORECASE)
            if match:
                triage_result = match.group(1)
                last_priority_idx = lines.index(line)
                break

    # Find the line that starts with 'Not Accepted'
    last_priority_idx = max(i for i, line in enumerate(lines)
                            if re.match(r"(Not Accepted):", line.strip(), re.IGNORECASE))

    # After finding that line we obtain the rationale
    rationale_lines = lines[last_priority_idx + 1:]
    rationale = " ".join(line.strip() for line in rationale_lines if line.strip())

    return {
        "result": triage_result, 
        "rationale": rationale
    }
    
# This function saves the results into our database
def results_to_db(ai_output: str, source_file: str):
    
    info = ai_output_info(ai_output)
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not set in environment.")

    engine = create_engine(DATABASE_URL)

    try:
        with engine.connect() as connection:
            sql_update_query = text("""
                UPDATE referral_triage_results
                SET result = :result,
                    rationale = :rationale
                WHERE source_file = :source_file
            """)
            connection.execute(sql_update_query, {
                "result": info["result"],
                "rationale": info["rationale"],
                "source_file": source_file
            })
            connection.commit() 
            #print(f"Successfully inserted triage results")
    except Exception as e:
        print(f"Error saving triage results")