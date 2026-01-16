from typing import TypedDict, Optional, Dict, Any
from langgraph.graph import StateGraph, END
from agent import email_agent
from tools import mock_send_email

# Define State Structure with explicit keys so values aggregate
class EmailState(TypedDict, total=False):
    input: Optional[str]
    email_data: Dict[str, Any]
    tool_result: Dict[str, Any]
    review_status: Optional[str]


def review_node(state: EmailState):
    # Automated review & sensitivity detection
    text_parts = []
    data = state.get("email_data")
    if data:
        text_parts.extend([str(data.get("subject", "")), str(data.get("body", ""))])
    if state.get("input"):
        text_parts.append(str(state.get("input")))

    text = " ".join(tp.lower() for tp in text_parts)

    # Refined spam logic: strong terms OR (CTA and promo/prize)
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
        status = "denied"
    elif is_sensitive:
        status = "needs-human"
    else:
        status = "approved"

    return {"review_status": status}


def send_email_node(state: EmailState):
    if state.get("review_status") == "denied":
        print("\n------ INCOMING EMAIL SKIPPED ------")
        print("Reason: Automated review classified as spam/denied.")
        print("---------------------------------\n")
        return {"tool_result": {"status": "Denied - Not Processed"}}

    data = state.get("email_data")
    if data is None:
        data = {
            "to": "hr@company.com",
            "subject": "Intern Application",
            "body": (state.get("input") or "No user input provided"),
        }

    result = mock_send_email(data)
    return {"tool_result": result}


# Build Graph
builder = StateGraph(EmailState)

builder.add_node("agent", email_agent)
builder.add_node("review", review_node)
builder.add_node("tools", send_email_node)

builder.set_entry_point("agent")

builder.add_edge("agent", "review")
builder.add_edge("review", "tools")
builder.add_edge("tools", END)

graph = builder
