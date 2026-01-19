from typing import TypedDict, Optional

class AgentState(TypedDict):
    email: str
    triage_decision: str
    reasoning: str
    human_decision: Optional[str]
