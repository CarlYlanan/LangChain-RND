import json 
import os 

FEEDBACK_FILE = "feedback_memory.json"

# Load feedback memory from JSON file
def loading_memory():
    # If file doesn't exist create an empty JSON list
    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w") as f:
            json.dump([], f)
        return []

    # If file exists but is empty, return an empty list
    if os.path.getsize(FEEDBACK_FILE) == 0:
        return []
    
    # Load and return existing JSON file 
    with open(FEEDBACK_FILE, "r") as f:
        return json.load(f)

# Adding new feedback into JSON file 
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

# Formatting feedback memory into examples for AI to interpret better
def build_feedback_examples(feedback_memory):
    examples = []
    
    for fb in feedback_memory:
        # Take first paragraph of referral summary from AI output
        referral_summary = fb["ai_triage_output"].split("\n\n")[0]
        ai_output = fb["ai_triage_output"] # Full AI triage output
        feedback = fb["feedback"] # Feedback reasoning
        final_decision = fb["final_decision"] # Final decision
        
        # Format the example in a way that AI can understand and learn
        example_text = (
            f"Example past case:\n"
            f"Referral summary: {referral_summary}\n"
            f"AI triage output: {ai_output}\n"
            f"Feedback: {feedback}\n"
            f"Final decision: {final_decision}\n"
        )
        
        # Add example to the list
        examples.append(example_text)
        
    # Join all examples together
    return "\n\n".join(examples)
