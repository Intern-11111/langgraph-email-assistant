from fastapi import APIRouter, HTTPException
from typing import Literal, Optional

from src.hitl.helpers import resume_with_decision

router = APIRouter(prefix="/hitl", tags=["HITL"])


@router.post("/decision")
def hitl_decision(
    thread_id: str,
    decision: Literal["approve", "deny", "edit"],
    edited_reply: Optional[str] = None,
):
    """
    Human-in-the-loop decision endpoint.

    IMPORTANT:
    - Paused state is immutable
    - Decisions are passed via graph.invoke(update, same thread_id)
    """

    # LOG: incoming HITL decision
    print("👤 HITL DECISION RECEIVED")
    print(f"   THREAD_ID : {thread_id}")
    print(f"   DECISION  : {decision}")

    if edited_reply:
        print(f" EDITED REPLY: {edited_reply}")

    # Validate EDIT input
    if decision == "edit" and not edited_reply:
        raise HTTPException(
            status_code=400,
            detail="edited_reply must be provided when decision is 'edit'",
        )

    # Resume graph with human decision
    resume_with_decision(
        thread_id=thread_id,
        decision=decision,
        edited_reply=edited_reply,
    )

    # DENY: terminal action
    if decision == "deny":
        print(" ACTION DENIED — execution stopped by human")
        return {
            "status": "DENIED",
            "message": "Action cancelled by human",
        }

    print(" GRAPH RESUMED AFTER HUMAN DECISION")

    return {
        "status": "RESUMED",
        "decision": decision,
    }
