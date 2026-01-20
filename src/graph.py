from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.state import AgentState
from src.nodes.node import (
    triage_node, check_route, ignore, notify_human, 
    react_model_node,react_tools_node,hitl_checkpoint,react_route
    
)


def create_graph():
    graph = StateGraph(AgentState)
    checkpointer = MemorySaver()
    
    graph.add_node("triage_node", triage_node)
    graph.add_node("ignore", ignore)
    graph.add_node("notify-human", notify_human)
    graph.add_node("react_model", react_model_node)  
    graph.add_node("react_tools", react_tools_node)  
    graph.add_node("hitl_checkpoint", hitl_checkpoint)

    # Edges
    graph.add_edge(START,"triage_node")
    graph.add_conditional_edges(
        "triage_node", check_route,
        {
            "ignore": "ignore", 
            "notify-human": "notify-human", 
            "respond-act": "react_model"
        }
    )
   
    # graph.add_conditional_edges(
    #     "react_model",
    #     lambda state:"hitl_checkpoint" if state.get("tool_name")=="send_email" else "react_tools",
    #     {"hitl_checkpoint": "hitl_checkpoint", "react_tools": "react_tools"}
    # )
    
    graph.add_conditional_edges(
    "react_model",
        react_route,
        {
            "hitl_checkpoint":"hitl_checkpoint",
            "react_tools": "react_tools",
            "react_end": END,
            "react_model": "react_model"
        }
    )

    graph.add_edge("react_tools", "react_model")
    graph.add_edge("hitl_checkpoint", "react_tools")
    #graph.add_edge("hitl_checkpoint", "hitl_handler")
    graph.add_edge("ignore", END)
    graph.add_edge("notify-human", END)
    #graph.add_edge("hitl_checkpoint", END) 
    return graph.compile(checkpointer=checkpointer,interrupt_before=["hitl_checkpoint"])

if __name__ == "__main__":
    create_graph()
    print("✅ Graph compiled successfully!")
