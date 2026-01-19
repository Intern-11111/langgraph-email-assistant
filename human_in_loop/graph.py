from langgraph.graph import StateGraph
from email_triage.state import AgentState
from email_triage.triage_agent import triage_email
from .pause_logic import pause_for_human

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("triage", triage_email)
    graph.add_node("pause", pause_for_human)
    graph.set_entry_point("triage")
    graph.add_edge("triage", "pause")
    return graph.compile()
