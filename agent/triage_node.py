def triage_email(state):
    email = state["email"]
    body = email["email_body"].lower()

    if "unsubscribe" in body or "sale" in body or "offer" in body:
        decision = "ignore"
    elif "complaint" in body or "legal" in body or "issue" in body:
        decision = "notify_human"
    else:
        decision = "respond"

    state["triage_decision"] = decision
    return state
