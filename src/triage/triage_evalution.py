import json
import os
import sys

from .triage_node import TriageNode

"""
This script evaluates TRIAGE ACCURACY.
It compares:
- agent triage output
vs
- human_label from dataset
"""

# ---------------------------
# Load golden dataset
# ---------------------------
def load_dataset(path="src/data/emails.json"):
    with open(path, "r") as f:
        return json.load(f)


# ---------------------------
# Calculate accuracy
# ---------------------------
def calculate_triage_accuracy():
    dataset = load_dataset()

    correct = 0
    total = len(dataset)

    triage = TriageNode()  

    for item in dataset:
        # Prepare input exactly like agent input
        state = {
            "email_text": {   
                "subject": item.get("subject", ""),
                "body": item.get("body", ""),
                "sender": item.get("sender", "")
            }
        }

        
        result_state = triage(state)
        agent_label = result_state["triage_result"]["final_label"]
        human_label = item.get("human_label")

        if agent_label == human_label:
            correct += 1

    accuracy = correct / total if total > 0 else 0

    print("========== TRIAGE EVALUATION ==========")
    print(f"Total Emails     : {total}")
    print(f"Correct Decisions: {correct}")
    print(f"Triage Accuracy  : {accuracy * 100:.2f}%")

    return accuracy


if __name__ == "__main__":
    calculate_triage_accuracy()
