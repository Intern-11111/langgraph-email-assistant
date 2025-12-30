from langsmith import traceable
from src.graph.state import EmailState
from src.config.smith import get_project_name

# -------------- Updated Keyword Rules (No ellipsis!) ----------------
RULE_IGNORE = [
    "viagra", "sex life", "unsubscribe", "lottery", "winner", "claim your prize",
    "limited time offer", "weight loss", "earn money fast", "cheap software"
]

RULE_RESPOND = [
    "meeting", "schedule", "reschedule", "call", "conference call",
    "agenda", "follow up", "follow-up", "can we", "please confirm"
]

RULE_NOTIFY = [
    "invoice", "payment", "approve", "approval", "signature", "contract",
    "legal", "complaint", "urgent", "security", "breach", "escalat",
    "audit", "finance", "vendor"
]

@traceable(name="triage_node", project_name=get_project_name())
def triage_email(state: EmailState) -> EmailState:

    text = (state.email_content or "").lower()

    if any(k in text for k in RULE_IGNORE):
        state.triage_decision = "ignore"
        state.triage_reason = "Spam / marketing detected"
        state.triage_confidence = 0.9
        return state

    if any(k in text for k in RULE_NOTIFY):
        state.triage_decision = "notify_human"
        state.triage_reason = "Sensitive or business-critical"
        state.triage_confidence = 0.85
        return state

    if any(k in text for k in RULE_RESPOND):
        state.triage_decision = "respond"
        state.triage_reason = "Normal coordination / scheduling"
        state.triage_confidence = 0.75
        return state

    state.triage_decision = "notify_human"
    state.triage_reason = "Unclear content — escalate to human"
    state.triage_confidence = 0.5
    return state
