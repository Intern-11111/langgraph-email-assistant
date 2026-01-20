from langchain_core.messages import BaseMessage
from typing import TypedDict,Literal,Annotated,Dict,Optional,Any,List
import operator

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage],operator.add]
    mail:dict
    triage_category: Literal["ignore", "notify-human", "respond-act"]
    tool_name: str           # which tool to call next (if any)
    tool_args: dict         # arguments for the tool
    final_reply: str        # drafted reply / action text
    hitl: Optional[Dict[str, Any]]   # {"tool": str, "args": dict, "proposed_reply": str | None, ...}
    hitl_decision: Optional[Literal["pending", "approve", "deny", "edit"]]