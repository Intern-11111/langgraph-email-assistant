def triage_node(state, model=None):
    subject = state["email"]["subject"].lower()
    body = state["email"]["body"].lower()

    text = subject + " " + body

    # -------- RULES --------

    # Dangerous → human
    danger_keywords = [
        "payment", "money", "bank", "legal", "contract",
        "delete", "transfer", "wire", "invoice"
    ]

    # Normal → respond
    respond_keywords = [
        "meeting", "update", "report", "share",
        "schedule", "confirm", "hello", "thanks"
    ]

    if any(k in text for k in danger_keywords):
        decision = "needs_human_review"

    elif any(k in text for k in respond_keywords):
        decision = "respond"

    else:
        decision = "needs_human_review"

    state["triage_decision"] = decision
    return state
