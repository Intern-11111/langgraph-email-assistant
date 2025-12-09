from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

device = "cuda" if torch.cuda.is_available() else "cpu"

triage_model = AutoModelForSequenceClassification.from_pretrained("./triage_model").to(device)
triage_tokenizer = AutoTokenizer.from_pretrained("./triage_model")
id2label = triage_model.config.id2label

PROMO_HINTS = [
    "unsubscribe", "newsletter", "sale", "promotion", "50% off",
    "flash sale", "digest", "recommended videos"
]

STATUS_HINTS = [
    "completed", "resolved", "report available", "policy update",
    "office closure", "backup completed", "deployment completed"
]

def triage_email(email):
    text = f"Subject: {email.get('subject','')}\n\n{email.get('body','')}"
    inputs = triage_tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=256
    ).to(device)

    with torch.no_grad():
        logits = triage_model(**inputs).logits
        probs = F.softmax(logits, dim=-1)[0].cpu().numpy()

    pred_id = int(probs.argmax())
    pred_label = id2label[pred_id]
    confidence = float(probs[pred_id])

    if pred_label == "ignore":
        reason = "Bulk or promotional style content; no clear action requested."
    elif pred_label == "notify_human":
        reason = "Status/update style email; important to see but no reply required."
    else:
        reason = "Email contains an explicit request for information, approval, or scheduling."

    return {
        "id": email.get("id"),
        "triage": pred_label,
        "confidence": confidence,
        "reason": reason
    }

def apply_rules_then_model(email):
    subject = (email.get("subject") or "").lower()
    body = (email.get("body") or "").lower()
    text = subject + " " + body

    if any(hint in text for hint in PROMO_HINTS):
        return {
            "id": email.get("id"),
            "triage": "ignore",
            "confidence": 0.95,
            "reason": "Matches promotional/newsletter keywords; safe to ignore."
        }

    if any(hint in text for hint in STATUS_HINTS):
        return {
            "id": email.get("id"),
            "triage": "notify_human",
            "confidence": 0.9,
            "reason": "Matches status/update keywords; user should be notified."
        }

    result = triage_email(email)

    if result["confidence"] < 0.6 and result["triage"] == "ignore":
        result["triage"] = "notify_human"
        result["reason"] = (
            "Model was uncertain; routing as notify_human to avoid missing important email."
        )

    return result


if __name__ == "__main__":
    sample_email = {
        "id": "test_001",
        "subject": "Need ETA on ViT ablation results",
        "from": "Engineering Manager <manager@company.com>",
        "body": "Hi Catherine,\nProduct wants to know when we can share preliminary results.\nCan you confirm if Friday works?\nThanks."
    }

    out = apply_rules_then_model(sample_email)
    print(out)
