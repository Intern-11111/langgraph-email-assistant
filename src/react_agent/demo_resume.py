from .state_utils import update_state


def demo_edit_and_resume(state):
    """
    Demonstrate editing draft before execution.
    """
    print("Original draft:", state.get("draft_response"))
    state = update_state(state, "Edited draft by human.")
    print("Updated draft:", state.get("draft_response"))
    return state
