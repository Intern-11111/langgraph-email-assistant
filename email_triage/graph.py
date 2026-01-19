from langgraph.graph import StateGraph
from .state import AgentState
from .triage_agent import triage_email

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("triage", triage_email)
    graph.set_entry_point("triage")
    return graph.compile()
