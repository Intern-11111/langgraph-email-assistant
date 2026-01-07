import sqlite3
import os

try:
    from langgraph.checkpoint.sqlite import SqliteSaver
    print("Checkpointer loaded successfully!")
except ImportError:
    print("Error: Package still not found. Try: 'python -m pip install langgraph-checkpoint-sqlite'")

from langgraph.graph import StateGraph, START, END
from state import AgentState
from node import (
    triage_node,
    check_route,
    react_route,
    ignore,
    notify_human,
    react_model_node,
    react_tools_node,
)

# --- PERSISTENCE (Memory) ---
# must save the agent's state(memory) to a database
db_path = "checkpoints.sqlite"
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

def graph_create() -> StateGraph:
    graph = StateGraph(AgentState)

    # ---NODES ---
    graph.add_node("triage_node", triage_node)
    graph.add_node("ignore", ignore)
    graph.add_node("notify-human", notify_human)
    graph.add_node("react_model", react_model_node)
    graph.add_node("react_tools", react_tools_node) 
    
    # ---EDGES ---
    graph.add_edge(START, "triage_node")

    graph.add_conditional_edges(
        "triage_node",
        check_route,
        {
            "ignore": "ignore",
            "notify-human": "notify-human",
            "respond-act": "react_model",
        },
    )

    graph.add_conditional_edges(
        "react_model",
        react_route,
        {
            "react_tools": "react_tools",
            "react_end": END,
            "react_model": "react_model",
        },
    )
    graph.add_edge("react_tools", "react_model")
    graph.add_edge("ignore", END)
    graph.add_edge("notify-human", END)

    # --- COMPILE WITH --- #
    return graph.compile(
        checkpointer=memory,
        interrupt_before=["react_tools"] 
    )

app = graph_create()

# --- RUN FUNCTION ---
def run_email_agent(subject: str, body: str, thread_id: str = "user_1"):
    config = {"configurable": {"thread_id": thread_id}}
    initial_state = {"mail": {"subject": subject, "body": body}}
    
    return app.invoke(initial_state, config=config)

