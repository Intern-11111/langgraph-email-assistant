from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any
"""
Here we create a one graph which is final workflow of agent where agent runs step by step 
"""

# Import nodes
from src.triage.triage_node import TriageNode
from src.agent.react_node import ReasonNode
from src.agent.tool_call import ToolExecutorNode

# ---------------------------
# 1. Define State Schema
# ---------------------------
class AgentState(TypedDict, total=False):
    email_text: Dict[str, Any]
    triage_result: Dict[str, Any]
    reasoning: list
    tool_result: Dict[str, Any]


# ---------------------------
# 2. Initialize Nodes
# ---------------------------
triage_node = TriageNode()
reason_node = ReasonNode()
tool_node = ToolExecutorNode()


# ---------------------------
# 3. Build Graph
# ---------------------------
graph = StateGraph(AgentState)

graph.add_node("triage", triage_node)
graph.add_node("reason", reason_node)
graph.add_node("act", tool_node)

graph.set_entry_point("triage")

graph.add_edge("triage", "reason")
graph.add_edge("reason", "act")
graph.add_edge("act", END)


# ---------------------------
# 4. Compile Graph
# ---------------------------
email_agent_graph = graph.compile()
