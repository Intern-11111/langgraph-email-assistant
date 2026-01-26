"""
LangGraph workflow for the email agent.
Simplified workflow using keyword-based categorization and templates (no LLM).
"""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from backend.src.state import AgentState
from backend.src.nodes.node import (
    triage_node, 
    check_route, 
    ignore, 
    notify_human,
    generate_response_node,
    hitl_checkpoint
)
import os


def create_graph(checkpointer=None):
    """
    Build the simplified email processing workflow.
    
    The workflow:
    1. Triage: Categorize email using keyword rules
    2. Route based on category:
       - ignore → Mark as processed
       - notify-human → Flag for human review
       - respond-act → Generate template response → HITL approval → Execute
    """
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("triage_node", triage_node)
    graph.add_node("ignore", ignore)
    graph.add_node("notify-human", notify_human)
    graph.add_node("generate_response", generate_response_node)
    graph.add_node("hitl_checkpoint", hitl_checkpoint)
    
    # Start with triage
    graph.add_edge(START, "triage_node")
    
    # Route based on categorization
    graph.add_conditional_edges(
        "triage_node",
        check_route,
        {
            "ignore": "ignore",
            "notify-human": "notify-human",
            "respond-act": "generate_response"
        }
    )
    
    # Response generation leads to HITL checkpoint (human approval)
    graph.add_edge("generate_response", "hitl_checkpoint")
    
    # After HITL approval, we're done
    graph.add_edge("hitl_checkpoint", END)
    
    # Direct end paths for ignore and notify-human
    graph.add_edge("ignore", END)
    graph.add_edge("notify-human", END)
    
    # Compile with HITL checkpoint (pause for human approval)
    return graph.compile(
        checkpointer=checkpointer,
        interrupt_before=["hitl_checkpoint"]
    )


# Create the default graph instance
email_assistance = create_graph()


if __name__ == "__main__":
    graph = create_graph()
    print("Simplified email agent graph compiled successfully!")
    print("Using keyword-based categorization and template responses (no LLM)")