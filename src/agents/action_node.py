from src.graph.state import EmailState


def action_node(state: EmailState) -> EmailState:
    """
    Executes the final action AFTER HITL approval.
    """

    print("ACTION NODE ENTERED")

    if state.human_decision == "deny":
        print("ACTION DENIED — no email sent")
        return state

    if state.human_decision == "edit":
        print("EMAIL SENT (EDITED BY HUMAN)")
        print("FINAL EMAIL CONTENT:")
        print(state.edited_reply)
        return state

    if state.human_decision == "approve":
        print("EMAIL SENT (AUTO-DRAFT APPROVED)")
        print("FINAL EMAIL CONTENT:")
        print(state.draft_reply)
        return state

    print("ACTION NODE REACHED WITHOUT HUMAN DECISION")
    return state
