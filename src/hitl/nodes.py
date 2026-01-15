from src.hitl.memory import save_state


def triage_node(state: dict):
    """
    Decide what to do with the email.
    """
    state["triage_decision"] = "respond"
    return state


def tool_node(state: dict):
    """
    Unsafe tool checkpoint.
    Execution pauses BEFORE any sensitive action.
    """

    print("\n⚠️ HUMAN APPROVAL REQUIRED ⚠️")
    print("Sensitive action detected: send_email")
    print("Agent execution paused before tool execution.")

    state["pending_tool"] = {
        "tool": "send_email",
        "status": "pending_approval"
    }

    save_state(state)
    state["paused"] = True
    return state
