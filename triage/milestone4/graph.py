from langgraph.graph import StateGraph, END
from agent import email_agent
from tools import mock_send_email

# Define State Structure
class EmailState(dict):
    pass


def send_email_node(state):
    result = mock_send_email(state["email_data"])
    return {"tool_result": result}


# Build Graph
builder = StateGraph(EmailState)

builder.add_node("agent", email_agent)
builder.add_node("tools", send_email_node)

builder.set_entry_point("agent")

builder.add_edge("agent", "tools")
builder.add_edge("tools", END)

graph = builder