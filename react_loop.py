import os
from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv()

# --------------------------------------------------
# 1. Define Agent State
# --------------------------------------------------
class AgentState(TypedDict):
    # Persistent message history (handled by MemorySaver)
    messages: Annotated[list, add_messages]


# --------------------------------------------------
# 2. Define Tools
# --------------------------------------------------
from tools.calendar import read_calendar
from tools.contacts import lookup_contact

tools = [read_calendar, lookup_contact]

# Flag unsafe tools (important for CLI approval step)
UNSAFE_TOOLS = {"send_email", "delete_file"}


# --------------------------------------------------
# 3. Setup LLM
# --------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)


# --------------------------------------------------
# 4. Define Graph Nodes
# --------------------------------------------------
def reason_node(state: AgentState):
    """
    The reasoning node:
    LLM decides whether to respond or call a tool.
    """
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def tool_executor_node(state: AgentState):
    """
    Executes tools requested by the LLM.
    """
    tool_node = ToolNode(tools)
    return tool_node.invoke(state)


# --------------------------------------------------
# 5. Conditional Routing Logic
# --------------------------------------------------
def should_continue(state: AgentState) -> Literal["tools", END]:
    """
    Decide whether to continue to tools or end execution.
    """
    last_message = state["messages"][-1]

    # If the LLM requested a tool → go to tools
    if last_message.tool_calls:
        return "tools"

    # Otherwise, we are done
    return END


# --------------------------------------------------
# 6. Build the Graph
# --------------------------------------------------
workflow = StateGraph(AgentState)

workflow.add_node("agent", reason_node)
workflow.add_node("tools", tool_executor_node)

workflow.add_edge(START, "agent")

workflow.add_conditional_edges(
    "agent",
    should_continue
)

workflow.add_edge("tools", "agent")


# --------------------------------------------------
# 7. Enable Memory + Interrupts (KEY MILESTONE STEP)
# --------------------------------------------------
memory = MemorySaver()

react_graph = workflow.compile(
    checkpointer=memory,           # ✅ Session memory
    interrupt_before=["tools"]     # ✅ Pause before tool execution
)
