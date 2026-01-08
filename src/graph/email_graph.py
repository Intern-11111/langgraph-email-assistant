from langgraph.graph import StateGraph

from src.graph.state import EmailState
from src.triage.triage_node import triage_email
from src.agents.react_loop import react_node
from src.graph.checkpoint import checkpointer


def action_node(state: EmailState) -> EmailState:
    """
    Action node where REAL-WORLD side effects happen.
    Execution reaches here ONLY after HITL approval.
    """

    # Explicit DENY
    if state.human_decision == "deny":
        print("ACTION NODE: Human denied action. No email sent.")
        return state

    # EDITED reply
    if state.human_decision == "edit":
        print("ACTION NODE: Sending EDITED email")
        print("EMAIL CONTENT:")
        print(state.edited_reply)
        return state

    # APPROVED reply
    if state.human_decision == "approve":
        print("ACTION NODE: Sending APPROVED email")
        print("EMAIL CONTENT:")
        print(state.draft_reply)
        return state

    # Safety fallback
    print("ACTION NODE reached without human decision")
    return state


def build_graph():
    """
    Milestone 3 LangGraph with HITL:

    triage → react → action_node (INTERRUPTED)
    """

    graph = StateGraph(EmailState)

    # Nodes
    graph.add_node("triage", triage_email)
    graph.add_node("react", react_node)
    graph.add_node("action_node", action_node)

    # Flow
    graph.set_entry_point("triage")
    graph.add_edge("triage", "react")
    graph.add_edge("react", "action_node")

    # HITL pause before irreversible action
    return graph.compile(
        checkpointer=checkpointer,
        interrupt_before=["action_node"]
    )
