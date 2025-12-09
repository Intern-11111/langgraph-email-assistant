from fastapi import APIRouter, Query
from datasets import load_dataset

from src.graph.email_graph import build_graph
from src.graph.state import EmailState

router = APIRouter()

# Build the LangGraph graph once at import time
graph = build_graph()

# ---------- Helper: load emails from Hugging Face ----------

NOTIFY_KEYWORDS = [
    "invoice", "payment", "approve", "approval", "signature", "contract", "legal",
    "complaint", "urgent", "security", "breach", "escalat", "audit", "finance",
    "vendor"
]


def map_label_from_spam(label: int, text: str) -> str:
    """
    Map HF spam/ham label into our triage labels:
    - spam (1)           -> ignore
    - ham (0, not spam)  -> respond OR notify_human based on keywords
    """
    text_l = text.lower()

    if label == 1:
        return "ignore"

    # ham → split into notify_human / respond
    if any(k in text_l for k in NOTIFY_KEYWORDS):
        return "notify_human"

    return "respond"


def load_hf_emails(limit: int = 10):
    """
    Load 'limit' emails from Hugging Face's Enron spam dataset
    and map them into our (email, label) format.
    """
    ds = load_dataset("SetFit/enron_spam")
    emails = []

    for idx, row in enumerate(ds["train"]):
        if idx >= limit:
            break

        # Try common column names: "email" or "text" or "message"
        text = (
            row.get("email")
            or row.get("text")
            or row.get("message")
            or ""
        )
        if not text:
            continue

        mapped_label = map_label_from_spam(row["label"], text)
        emails.append(
            {
                "email": text,
                "label": mapped_label,         # our triage label
                "source_label": row["label"],  # original spam/ham
            }
        )

    return emails


# ---------- API ENDPOINTS ----------

@router.get("/data")
def get_hf_data(limit: int = Query(10, ge=1, le=100)):
    """
    Return raw email text + mapped triage labels from Hugging Face.
    """
    samples = load_hf_emails(limit)
    return {
        "count": len(samples),
        "samples": samples,
    }


@router.get("/triage")
def triage_hf_emails(limit: int = Query(10, ge=1, le=100)):
    """
    Run the LangGraph triage agent on Hugging Face emails
    and compare predicted vs mapped labels.
    """
    samples = load_hf_emails(limit)
    results = []
    correct = 0

    for item in samples:
        state = EmailState(email_content=item["email"])
        output = graph.invoke(state)  # LangGraph returns a dict-like state

        predicted = output.get("triage_decision")
        gold = item["label"]

        if predicted == gold:
            correct += 1

        email_text = item["email"]
        preview = email_text[:120] + ("..." if len(email_text) > 120 else "")

        results.append(
            {
                "email_preview": preview,
                "gold_label": gold,
                "predicted_label": predicted,
                "triage_reason": output.get("triage_reason"),
            }
        )

    accuracy = correct / len(samples) if samples else 0.0

    return {
        "count": len(samples),
        "accuracy": accuracy,
        "results": results,
    }
