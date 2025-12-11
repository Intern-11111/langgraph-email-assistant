from langchain_core.messages import BaseMessage
from typing import TypedDict,Literal,Annotated
import operator

class AgentState(TypedDict):
    message: Annotated[list[BaseMessage],operator.add]
    mail:dict
    triage_category: Literal["ignore", "notify_human", "respond_act"]


    pass