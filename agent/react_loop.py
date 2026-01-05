# Agent flow : Email → Reason → Tool → Observe → Repeat → Draft Reply
def react_agent(state):
    email = state["email"]
    body = email["email_body"].lower()

    if "meeting" in body:
        reply = (
            "Thanks for reaching out. "
            "I am available tomorrow between 2 PM and 5 PM. "
            "Please let me know what works for you."
        )
    elif "report" in body:
        reply = "I will review the report and get back to you shortly."
    else:
        reply = "Thank you for your email. I will respond soon."

    state["agent_reply"] = reply
    return state
