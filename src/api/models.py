from typing import Optional, Literal, List
from pydantic import BaseModel, Field


class EmailRequest(BaseModel):
    """
    Request body for the /triage/email endpoint.
    """
    email: str = Field(
        ...,
        description="Raw email text that should be triaged."
    )


class TriageResult(BaseModel):
    """
    Core triage output: what to do with this email.
    """
    decision: Literal["ignore", "notify_human", "respond"] = Field(
        ...,
        description="Triage decision for the email."
    )
    reason: Optional[str] = Field(
        default=None,
        description="Short explanation of why this decision was made."
    )
    confidence: Optional[float] = Field(
        default=None,
        description="Optional confidence score between 0 and 1."
    )


class BatchTriageResponse(BaseModel):
    """
    Optional: used if you later add batch triage endpoints.
    Not mandatory right now, but handy for HF triage, etc.
    """
    count: int
    results: List[TriageResult]
