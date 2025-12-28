from langgraph.graph import StateGraph, END
from state import EmailState
from triage import triage_node
from agent import agent_node

graph = StateGraph(EmailState)

# Nodes
graph.add_node("triage", triage_node)
graph.add_node("agent", agent_node)

# Entry
graph.set_entry_point("triage")

# Routing logic
def route_after_triage(state):
    if state["category"] == "respond":
        return "agent"
    return END

graph.add_conditional_edges("triage", route_after_triage)
graph.add_edge("agent", END)

app = graph.compile()
