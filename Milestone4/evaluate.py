import json
from collections import Counter
from pathlib import Path


def detect_status(subject: str, body: str) -> str:
    text = f"{subject} {body}".lower()

    cta_terms = [
        "click here", "click on the link", "click the link", "click link",
        "claim", "buy now", "act now", "claim now"
    ]
    promo_terms = [
        "free", "congratulations", "limited time", "offer", "sale", "discount", "bonus", "gift"
    ]
    prize_terms = ["lottery", "prize", "winner", "win money"]
    strong_spam_terms = [
        "viagra", "xxx", "crypto double", "investment scheme", "rich quick", "credit card"
    ]

    has_cta = any(t in text for t in cta_terms)
    has_promo = any(t in text for t in promo_terms)
    has_prize = any(t in text for t in prize_terms)
    has_strong_spam = any(t in text for t in strong_spam_terms)

    is_spam = has_strong_spam or ((has_cta) and (has_promo or has_prize)) or ("100% free" in text)

    sensitive_markers = [
        "approve", "approval", "urgent", "payment", "salary", "confidential",
        "escalate", "legal", "contract", "offer letter", "promotion",
        "termination", "invoice", "wire", "receipt", "due", "bill",
        "bank", "account", "security", "transaction"
    ]

    is_sensitive = any(m in text for m in sensitive_markers)
    if is_spam:
        return "denied"
    if is_sensitive:
        return "needs-human"
    return "approved"


def map_label_to_status(label: str) -> str:
    # Assumptions for evaluation mapping:
    # - spam -> denied
    # - finance -> needs-human (potentially sensitive)
    # - others -> approved (non-sensitive)
    if label == "spam":
        return "denied"
    if label == "finance":
        return "needs-human"
    return "approved"


def main():
    data_path = Path(__file__).resolve().parents[1] / "data" / "golden_emails.json"
    with open(data_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    totals = 0
    correct = 0
    per_class = Counter()
    confusion = Counter()

    for item in items:
        subject = item.get("subject", "")
        body = item.get("body", "")
        human_label = (item.get("human_label") or "").lower()

        y_true = map_label_to_status(human_label)
        y_pred = detect_status(subject, body)

        totals += 1
        if y_true == y_pred:
            correct += 1
        per_class[("true", y_true)] += 1
        per_class[("pred", y_pred)] += 1
        confusion[(y_true, y_pred)] += 1

    accuracy = correct / totals if totals else 0.0

    print("=== Evaluation (Incoming Email Classification) ===")
    print(f"Total: {totals}")
    print(f"Quality rate (accuracy): {accuracy:.2%}")
    print("\nPer-class totals:")
    for cls in ["denied", "needs-human", "approved"]:
        true_count = per_class.get(("true", cls), 0)
        pred_count = per_class.get(("pred", cls), 0)
        print(f"- True {cls}: {true_count}; Pred {cls}: {pred_count}")

    print("\nConfusion matrix (true -> pred):")
    for t in ["denied", "needs-human", "approved"]:
        row = [confusion.get((t, p), 0) for p in ["denied", "needs-human", "approved"]]
        print(f"{t:13s} -> {row}")


if __name__ == "__main__":
    main()
