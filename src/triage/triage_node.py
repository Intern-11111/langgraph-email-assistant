from langsmith import traceable
from src.graph.state import EmailState
from src.config.smith import get_project_name


# Very simple keyword-based rules for Milestone 1
IGNORE_KEYWORDS = [
    "viagra", "sex life", "software just for", "cheap software",
    "unsubscribe", "lottery", "winner", "claim your prize",
    "limited time offer", "weight loss", "earn money fast",
]

RESPOND_KEYWORDS = [
    "meeting", "schedule", "reschedule", "call", "conference call",
    "agenda", "follow up", "follow-up", "can we", "please confirm",
]

NOTIFY_KEYWORDS = [
    "invoice", "payment", "approve", "approval", "signature", "contract",
    "legal", "complaint", "urgent", "security", "breach", "escalat",
    "audit", "finance", "vendor",
]


@traceable(name="triage_node", project_name=get_project_name())
def triage_email(state: EmailState) -> EmailState:
    """
    Heuristic / rule-based triage for Milestone 1.

    This does NOT depend on the LLM, which keeps behavior stable
    even with a tiny free model.

    Rules:
    - If spammy keywords -> ignore
    - Else if critical/business keywords -> notify_human
    - Else if conversational / scheduling -> respond
    - Else -> notify_human (conservative)
    """

    text = (state.email_content or "").lower()

    # 1) Obvious spam / marketing → ignore
    if any(k in text for k in IGNORE_KEYWORDS):
        state.triage_decision = "ignore"
        state.triage_reason = "Heuristic: email matches spam/marketing patterns."
        state.triage_confidence = 0.9
        return state

    # 2) Critical / sensitive content → notify_human
    if any(k in text for k in NOTIFY_KEYWORDS):
        state.triage_decision = "notify_human"
        state.triage_reason = "Heuristic: email mentions sensitive business/finance/legal terms."
        state.triage_confidence = 0.8
        return state

    # 3) Normal work / coordination → respond
    if any(k in text for k in RESPOND_KEYWORDS):
        state.triage_decision = "respond"
        state.triage_reason = "Heuristic: email looks like a normal coordination / meeting request."
        state.triage_confidence = 0.75
        return state

    # 4) Default: conservative → notify_human
    state.triage_decision = "notify_human"
    state.triage_reason = "Heuristic fallback: could not clearly classify; escalating to human."
    state.triage_confidence = 0.5
    return state
