from langchain_core.messages import BaseMessage
from typing import TypedDict,Literal,Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage],operator.add]
    mail:dict
    triage_category: Literal["ignore", "notify-human", "respond-act"]
