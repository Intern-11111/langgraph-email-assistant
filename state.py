# from typing import TypedDict, List

# class AgentState(TypedDict):
#     email: str
#     decision: str
#     thoughts: List[str]
from typing import TypedDict, List

class EmailState(TypedDict):
    email: str
    category: str
    thoughts: List[str]
    reply: str

