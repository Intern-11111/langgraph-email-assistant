# graph.py

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.agent.react_node import ReasonNode
from src.triage.triage_node import TriageNode
from src.HITL.execute_tool import ToolExecutorNode

def build_graph():
    graph = StateGraph(dict)

    graph.add_node("triage", TriageNode())
    graph.add_node("reason", ReasonNode())
    graph.add_node("tool", ToolExecutorNode())

    graph.set_entry_point("triage")
    graph.add_edge("triage", "reason")
    graph.add_edge("reason", "tool")
    graph.add_edge("tool", END)

    return graph.compile(
        checkpointer=MemorySaver(),
        interrupt_after=["tool"]  
    )