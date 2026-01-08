from src.graph.email_graph import build_graph

# Build the LangGraph ONCE per process
_graph = build_graph()


def get_graph():
    """
    Return the singleton LangGraph instance.
    """
    return _graph
