from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from backend.src.state import AgentState
from backend.src.nodes.node import (
    triage_node, check_route, ignore, notify_human, 
    react_model_node,react_tools_node,hitl_checkpoint,react_route
    
)
import sqlite3
import os
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

DB_PATH = os.getenv("DB_PATH", "data/checkpoints.db")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def create_graph(checkpointer=None):
    """
    Builds the email agent's workflow graph. Here's how it works:
    
    1. START -> triage_node: AI reads the email and decides what category it is
    2. Based on category:
       - ignore: Mark as read and END
       - notify-human: Add label for human review and END
       - respond-act: Generate a draft response
    
    3. For respond-act emails, we enter a ReAct loop:
       - react_model: AI decides next action (call tool / draft reply / done)
       - react_tools: If AI wants to call a tool, run it here
       - hitl_checkpoint: Pause for human approval before sending
       - Loop continues until final reply is ready
    
    The graph pauses at hitl_checkpoint so humans can review drafts before sending.
    """
    graph = StateGraph(AgentState)

    # Add all the nodes (each node is a step in the workflow)
    graph.add_node("triage_node", triage_node)
    graph.add_node("ignore", ignore)
    graph.add_node("notify-human", notify_human)
    graph.add_node("react_model", react_model_node)  
    graph.add_node("react_tools", react_tools_node)  
    graph.add_node("hitl_checkpoint", hitl_checkpoint)

    # Start by triaging the email
    graph.add_edge(START,"triage_node")
    
    # Route based on triage decision
    graph.add_conditional_edges(
        "triage_node", check_route,
        {
            "ignore": "ignore", 
            "notify-human": "notify-human", 
            "respond-act": "react_model"
        }
    )
    
    # ReAct loop routing logic
    graph.add_conditional_edges(
    "react_model",
        react_route,
        {
            "hitl_checkpoint":"hitl_checkpoint",  # Need human approval
            "react_tools": "react_tools",  # Call a tool
            "react_end": END,  # Done
            "react_model": "react_model"  # Continue thinking
        }
    )

    # After calling a tool, route through react_route to check if we should end
    # This was previously a fixed edge to react_model which caused infinite loops
    # graph.add_conditional_edges(
    #     "react_tools",
    #     react_route,
    #     {
    #         "hitl_checkpoint": "hitl_checkpoint",
    #         "react_tools": "react_tools",
    #         "react_end": END,
    #         "react_model": "react_model"
    #     }
    # )

    graph.add_edge("react_tools", "react_model")
    
    # After human approves, continue to tools (which will send the email)
    graph.add_edge("hitl_checkpoint", "react_tools")
    
    # Terminal nodes
    graph.add_edge("ignore", END)
    graph.add_edge("notify-human", END)
    
    # Compile with interrupt at human approval checkpoint
    return graph.compile(checkpointer=checkpointer,interrupt_before=["hitl_checkpoint"])

email_assistance=create_graph()

if __name__ == "__main__":
    create_graph()
    print("Graph compiled successfully!")