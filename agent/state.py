from typing import TypedDict, Optional

class AgentState(TypedDict):
    email: dict
    triage_decision: Optional[str]
    agent_reply: Optional[str]
