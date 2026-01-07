from langgraph.graph import StateGraph
from src.hitl.nodes import triage_node, action_node, checkpoint_node

def build_hitl_graph():
    graph = StateGraph(dict)

    graph.add_node("triage_node", triage_node)
    graph.add_node("checkpoint", checkpoint_node)
    graph.add_node("action_node", action_node)

    graph.set_entry_point("triage_node")

    graph.add_edge("triage_node", "checkpoint")
    graph.add_edge("checkpoint", "action_node")

    return graph.compile(
        interrupt_before=["action_node"]  # 🔴 HITL happens here
    )
