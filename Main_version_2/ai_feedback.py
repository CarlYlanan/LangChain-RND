import json 
import os 

FEEDBACK_FILE = "feedback_memory.json"

def loading_memory():
    
    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w") as f:
            json.dump([], f)
        return []

    if os.path.getsize(FEEDBACK_FILE) == 0:
        return []
    
    with open(FEEDBACK_FILE, "r") as f:
        return json.load(f)
    
def accepting_feedback(file_name, ai_triage_output, feedback, final_decision):
    data = loading_memory()
    data.append({
        "file_name": file_name, 
        "ai_triage_output": ai_triage_output, 
        "feedback": feedback, 
        "final_decision": final_decision
    })
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_feedback_context():
    feedback_results = loading_memory()
    if not feedback_results:
        return "No memory can be found."
    
    context = "Here is the latest feedback correction:\n\n"
    for fb in feedback_results[-1:]:
        context += f"- File: {fb['file_name']}, Correction: {fb['final_decision']} (Reason: {fb['feedback']})\n"
    
    return context