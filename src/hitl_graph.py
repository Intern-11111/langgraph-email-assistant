from typing import TypedDict
from langgraph.graph import StateGraph, END

from src.tools_hitl import (
    read_email,
    read_calendar,
    send_email,
    create_calendar_invite
)
from src.hitl_guard import check_hitl


class AgentState(TypedDict):
    tool_name: str
    tool_input: str
    result: str


def execute_tool(state: AgentState):
    tool = state["tool_name"]
    tool_input = state["tool_input"]

    # ---------------- HITL CHECK ----------------
    check_hitl(tool, tool_input)

    # ---------------- TOOL EXECUTION ----------------
    if tool == "read_email":
        return {"result": read_email.invoke({})}

    if tool == "read_calendar":
        return {"result": read_calendar.invoke({})}

    if tool == "send_email":
        return {"result": send_email.invoke({"content": tool_input})}

    if tool == "create_calendar_invite":
        return {"result": create_calendar_invite.invoke({"details": tool_input})}

    return {"result": "Unknown tool"}


def build_hitl_graph():
    graph = StateGraph(AgentState)
    graph.add_node("execute_tool", execute_tool)
    graph.set_entry_point("execute_tool")
    graph.add_edge("execute_tool", END)
    return graph.compile()
