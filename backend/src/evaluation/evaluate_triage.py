import json
from triage.triage_node import triage_email
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
    print("\nFinal Accuracy:", round(accuracy, 2))

    # confusion matrix
    print("\nCONFUSION MATRIX (simple)")
    print(confusion_matrix(y_true, y_pred, labels=labels))


if __name__ == "__main__":
    evaluate()