def inspect_state(state):
    """
    Inspect current agent state.
    """
    return state


def update_state(state, new_text):
    """
    Update draft response in state.
    """
    state["draft_response"] = new_text
    return state
