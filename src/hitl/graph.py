from langgraph.graph import StateGraph
from src.hitl.nodes import triage_node, tool_node


def build_hitl_graph():
    """
    LangGraph with unsafe tool interruption (Milestone 4)
    """

    graph = StateGraph(dict)

    graph.add_node("triage_node", triage_node)
    graph.add_node("tools", tool_node)

    graph.set_entry_point("triage_node")
    graph.add_edge("triage_node", "tools")

    # 🔴 Milestone-4 requirement
    return graph.compile(
        interrupt_before=["tools"]
    )
