from src.hitl.memory import save_state

def triage_node(state):
    # Normally comes from Milestone-1
    state["triage_decision"] = "needs_human_review"
    return state

def action_node(state):
    state["final_action"] = f"Action taken for {state['triage_decision']}"
    return state

def checkpoint_node(state):
    # HITL checkpoint: save state and pause
    save_state(state)
    state["paused"] = True
    return state
