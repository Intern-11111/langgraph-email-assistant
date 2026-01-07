from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # This stores the conversation history
    messages: Annotated[list, add_messages]
    # This stores the email data
    mail: dict 
    # This stores the triage result (e.g., "ignore" or "respond")
    triage_category: str
    final_reply: str
