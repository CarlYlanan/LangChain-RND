import json 
import os 

feedback_file = "feedback_memory.json"

def loading_memory():
    if os.path.exists(feedback_file):
        with open(feedback_file, "r") as f:
            return json.load(f)
        return [] 
    
def accepting_feedback(file_name, ai_output, feedback, final_decision):
    data = loading_memory()
    data.append({
        "file_name": file_name, 
        "ai_output": ai_output, 
        "feedback": feedback, 
        "final_decision": final_decision
    })
    with open(feedback_file, "w") as f:
        json.dumpe(data, f, indent=2)

def get_feedback_context():
    feedback_results = loading_memory()
    if not feedback_results:
        return "No memory can be found."
    context = "Here is the lastest feedback correction:\n\n"
    for fb in feedback_results[-1:]:
        content += f"- File: {fb['file_name']}, Correction: {fb['final_label']} (Reason: {fb['feedback']})\n"
        return context