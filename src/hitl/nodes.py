def checkpoint_node(state):
    """
    HITL checkpoint node.
    """
    state["paused"] = True
    return state
