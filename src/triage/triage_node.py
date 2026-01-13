def triage_node(state: dict, model):
    """
    state = {
        "email": {
            "subject": "...",
            "body": "..."
        }
    }
    """

    email_text = state["email"]["subject"] + " " + state["email"]["body"]
    decision = model.predict([email_text])[0]

    state["triage_decision"] = decision
    return state
