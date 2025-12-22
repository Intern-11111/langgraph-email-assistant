from typing import TypedDict, List

class AgentState(TypedDict):
    email: str
    decision: str
    thoughts: List[str]
