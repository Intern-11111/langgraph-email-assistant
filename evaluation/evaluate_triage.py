import json
# try robust imports for triage_email
try:
    from triage.triage_node import triage_email
except Exception:
    try:
        # try importing by module name (useful if running from project root)
        from triage_node import triage_email
    except Exception:
        # add project root to sys.path and retry
        import os, sys
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        try:
            from triage.triage_node import triage_email
        except Exception as e:
            raise ImportError("Could not import triage_email. Ensure triage package or triage_node.py exists.") from e
from sklearn.metrics import confusion_matrix

def load_dataset():
    with open("data/golden_emails.json") as f:
        return json.load(f)

def evaluate():
    data = load_dataset()

    labels = ["spam", "promotion", "normal", "action_intent", "unknown"]

    y_true = []
    y_pred = []

    # class count
    counts = {l: 0 for l in labels}

    for item in data:
        email = item["email"]
        actual = item["label"]

        predicted = triage_email(email)

        y_true.append(actual)
        y_pred.append(predicted)

        if predicted in counts:
            counts[predicted] += 1
        else:
            counts["unknown"] += 1

    # ---- PRINT CLEAN SUMMARY ----
    print("\nCATEGORY COUNTS")
    for k, v in counts.items():
        print(f"{k}: {v}")

    # accuracy
    accuracy = sum([1 for a, b in zip(y_true, y_pred) if a == b]) / len(y_true)
    print(f"\nFinal Accuracy: {accuracy*100:.1f}%")

    # confusion matrix
    print("\nCONFUSION MATRIX (simple)")
    print(confusion_matrix(y_true, y_pred, labels=labels))


if __name__ == "__main__":
    evaluate()