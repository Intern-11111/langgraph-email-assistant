"""
State management for the email agent.
Simplified for template-based workflow (no LLM conversation history needed).
"""
from typing import TypedDict, Literal, Dict, Optional, Any

class AgentState(TypedDict):
    """
    This is what the agent remembers as it processes each email.
    Think of it like the agent's notepad that gets passed around.
    """
    mail: dict  # The email being processed: {id, subject, sender, body, thread_id}
    userid: str  # Which user this email belongs to
    triage_category: Literal["ignore", "notify-human", "respond-act"]  # What the agent decided to do
    action_type: Optional[str]  # What action to take (send_reply, create_calendar, etc.)
    action_args: Optional[dict]  # Arguments for that action
    final_reply: Optional[str]  # The drafted email response (template-based)
    tool_result: Optional[Any]  # Result of the tool execution (e.g. success message)
    hitl: Optional[Dict[str, Any]]  # Human-in-the-loop data for approval
    hitl_decision: Optional[Literal["pending", "approve", "deny", "edit", "processed"]]  # What the human decided
