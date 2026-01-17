from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any

from typing import List


class EmailState(BaseModel):
    # INPUT
    email_content: str

    # 🔥 REAL EMAIL METADATA
    from_email: Optional[str] = None
    subject: Optional[str] = None


    # TRIAGE
    triage_decision: Optional[Literal["ignore", "notify_human", "respond"]] = None
    triage_reason: Optional[str] = None
    triage_confidence: Optional[float] = None


    # LLM METADATA (Milestone 2)
    llm_intent: Optional[str] = None
    llm_confidence: Optional[float] = None

    # REPLY GENERATION
    agent_thoughts: Optional[str] = None
    draft_reply: Optional[str] = None

    # QUALITY / EVAL SIGNALS
    reply_quality: Optional[float] = None

    # HITL (Milestone 3)
    hitl_required: bool = False
    human_decision: Optional[Literal["approve", "deny", "edit"]] = None
    edited_reply: Optional[str] = None

    # ACTION PLANNING (Milestone 4)
    selected_tool: Optional[
        Literal[
            "send_email",
            "create_calendar_event",
            "read_email",
            "read_calendar",
        ]
    ] = None

    tool_payload: Optional[Dict[str, Any]] = None

    # EXECUTION STATUS (NEW – IMPORTANT)
    action_executed: bool = False
    action_error: Optional[str] = None
    execution_logs: List[str] = []