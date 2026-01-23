def approval_node(state, user_action=None, edited_text=None):
    """
    Handles human approval logic.
    user_action: 'approve', 'deny', or 'edit'
    """

    # Pause state
    state["paused"] = True

    if user_action is None:
        # No input yet → just pause
        return state

    if user_action == "approve":
        state["paused"] = False
        state["approved"] = True

    elif user_action == "deny":
        state["paused"] = False
        state["approved"] = False
        state["draft_response"] = "Action denied by user."

    elif user_action == "edit":
        state["paused"] = False
        state["approved"] = True
        if edited_text:
            state["draft_response"] = edited_text

    return state
