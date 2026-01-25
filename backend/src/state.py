from langchain_core.messages import BaseMessage
from typing import TypedDict,Literal,Annotated,Dict,Optional,Any,List
import operator

class AgentState(TypedDict):
    """
    This is what the AI agent remembers as it processes each email.
    Think of it like the agent's notepad that gets passed around.
    """
    messages: Annotated[list[BaseMessage], operator.add]  # Conversation history with the LLM
    mail: dict  # The email being processed: {id, subject, sender, body, thread_id}
    userid: str  # Which user this email belongs to
    triage_category: Literal["ignore", "notify-human", "respond-act"]  # What the AI decided to do
    tool_name: Optional[str]  # If the AI needs to call a tool, which one?
    tool_args: Optional[dict]  # Arguments for that tool
    final_reply: Optional[str]  # The drafted email response
    hitl: Optional[Dict[str, Any]]  # Human-in-the-loop data for approval
    hitl_decision: Optional[Literal["pending", "approve", "deny", "edit"]]  # What the human decided
