# src/graph/graph_registry.py
from src.graph.email_graph import build_graph
from src.graph.checkpoint import checkpointer

_graph = None

def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph(checkpointer=checkpointer)
    return _graph
