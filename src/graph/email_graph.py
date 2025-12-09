from langgraph.graph import StateGraph
from src.graph.state import EmailState
from src.triage.triage_node import triage_email
from src.agents.react_loop import react_node


def build_graph():
    """
    Build the LangGraph for Milestone 1:

    triage → react

    - triage: decides ignore / notify_human / respond
    - react: only runs if decision == 'respond', drafts reply
    """
    graph = StateGraph(EmailState)

    # Nodes
    graph.add_node("triage", triage_email)
    graph.add_node("react", react_node)

    # Flow: triage → react
    graph.set_entry_point("triage")
    graph.add_edge("triage", "react")

    # let graph end after react by default
    return graph.compile()
