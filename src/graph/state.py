from pydantic import BaseModel, Field
from typing import Optional, Literal

class EmailState(BaseModel):
    # Input
    email_content: str = Field(...)

    # Triage decision
    triage_decision: Optional[Literal["ignore", "notify_human", "respond"]] = None
    triage_reason: Optional[str] = None
    triage_confidence: Optional[float] = None

    # 🔥 Milestone 2 extra metadata
    llm_intent: Optional[str] = None
    llm_confidence: Optional[float] = None

    # Reply-for-respond
    agent_thoughts: Optional[str] = None
    draft_reply: Optional[str] = None

    # Evaluation Quality Signals
    reply_quality: Optional[float] = None

    # HITL fields
    hitl_required: bool = False
    human_decision: Optional[Literal["approve", "deny", "edit"]] = None
    edited_reply: Optional[str] = None

    # Planned action
    selected_tool: Optional[str] = None
    tool_payload: Optional[dict] = None
