# graph.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from state import EmailState
from triage import triage_node
from agent import agent_node

def build_graph():

    graph = StateGraph(EmailState)

    # Nodes
    graph.add_node("triage", triage_node)
    graph.add_node("agent", agent_node)

    # Entry point
    graph.set_entry_point("triage")

    # Routing after triage
    def route_after_triage(state):
        if state["category"] == "respond":
            return "agent"
        return END

    graph.add_conditional_edges("triage", route_after_triage)
    graph.add_edge("agent", END)

    # Checkpointing (LangSmith + HITL ready)
    memory = MemorySaver()

    app = graph.compile(
        checkpointer=memory
    )

    return app
