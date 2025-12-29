import json
from .triage_node import TriageNode

# ---------------------------
# Load dataset
# ---------------------------
def load_dataset(path="src/data/emails.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------------
# Calculate accuracy
# ---------------------------
def calculate_triage_accuracy():
    dataset = load_dataset()

    correct = 0
    total = len(dataset)

    triage = TriageNode()

    for idx, item in enumerate(dataset, start=1):

        state = {
            "email_text": {
                "subject": item.get("subject", ""),
                "body": item.get("body", ""),
                "sender": item.get("sender", "")
            }
        }

        result_state = triage(state)

        agent_label = (
            result_state["triage_result"]["final_label"] .strip() .lower() )

        triage_label = (
            item.get("triage_label") .strip() .lower())

        if agent_label == triage_label:
            correct += 1
        else:
            # optional debug
            # print(f"❌ {idx}: agent={agent_label}, human={human_label}")
            pass

    accuracy = correct / total if total > 0 else 0

    print("\n========== TRIAGE EVALUATION ==========")
    print(f"Total Emails     : {total}")
    print(f"Correct Decisions: {correct}")
    print(f"Triage Accuracy  : {accuracy * 100:.2f}%")

    return accuracy

# ---------------------------
# Entry point
# ---------------------------
if __name__ == "__main__":
    calculate_triage_accuracy()

