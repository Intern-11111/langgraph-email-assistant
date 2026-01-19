from langgraph.graph import StateGraph
from .tools import send_email_tool
from .pause import pause_before_tool

def build_graph():
    graph = StateGraph(dict)

    graph.add_node("pause", pause_before_tool)
    graph.add_node("tools", send_email_tool)

    graph.set_entry_point("pause")
    graph.add_edge("pause", "tools")

    # 🔥 IMPORTANT: interrupt before tools execute
    return graph.compile(
        interrupt_before=["tools"]
    )
