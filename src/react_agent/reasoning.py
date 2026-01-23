def reasoning_node(state):
    """
    Agent reasoning step.
    Creates a draft response based on triage decision.
    """

    decision = state.get("triage_decision")

    if decision == "respond":
        state["draft_response"] = (
            "Draft: Respond to the email politely and provide the update."
        )
    else:
        state["draft_response"] = (
            "Draft: Ask for more clarification from the sender."
        )

    return state
