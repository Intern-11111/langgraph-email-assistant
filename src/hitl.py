"""
HITL decision handler for Milestone 4.

Controls whether a dangerous action
is allowed to execute.
"""

def handle_hitl_decision(user_choice, tool_fn, *args):
    if user_choice == "approve":
        print("HITL: Approved by human")
        return tool_fn(*args)

    if user_choice == "deny":
        print("HITL: Action denied by human")
        return "execution_blocked"

    print("HITL: Invalid human decision")
    return "invalid_decision"
