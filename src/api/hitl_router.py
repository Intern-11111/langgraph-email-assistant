from fastapi import APIRouter, HTTPException
from typing import Literal, Optional
import re

from src.memory.store import save_memory
from src.hitl.helpers import resume_with_decision
from src.graph.graph_registry import get_graph

router = APIRouter(prefix="/hitl", tags=["HITL"])

graph = get_graph()


def extract_name_preference(text: str) -> Optional[str]:
    """
    Extract name preference from text.
    Examples:
    - "Call me Robert"
    - "Please refer to me as Michael"
    - "My name is Alex"
    """
    patterns = [
        r"call me (\w+)",
        r"refer to me as (\w+)",
        r"my name is (\w+)",
    ]

    text_l = text.lower()

    for p in patterns:
        match = re.search(p, text_l)
        if match:
            return match.group(1).capitalize()

    return None


@router.post("/decision")
def hitl_decision(
    thread_id: str,
    decision: Literal["approve", "deny", "edit"],
    edited_reply: Optional[str] = None,
    to: Optional[str] = None,
    subject: Optional[str] = None,
):
    """
    Human-in-the-loop decision endpoint.
    Memory is written ONLY on human approval.
    """

    if decision == "edit" and not edited_reply:
        raise HTTPException(
            status_code=400,
            detail="edited_reply must be provided when decision is 'edit'",
        )

    # ---------------- MEMORY SAVE (HITL-GATED) ----------------
    if decision == "approve":
        try:
            # Pull latest paused state
            state = graph.get_state(
                config={"configurable": {"thread_id": thread_id}}
            ).values

            source_text = (
                state.get("email_content", "")
                + "\n"
                + state.get("draft_reply", "")
            )

            preferred_name = extract_name_preference(source_text)

            if preferred_name:
                save_memory(
                    namespace="preferences",
                    key="name",
                    value=preferred_name,
                )
                print(f" MEMORY SAVED → preferred_name = {preferred_name}")

        except Exception as e:
            print(" Memory extraction failed:", str(e))

    # ---------------- RESUME GRAPH ----------------
    resume_with_decision(
        thread_id=thread_id,
        decision=decision,
        edited_reply=edited_reply,
        to=to,
        subject=subject,
    )

    if decision == "deny":
        return {
            "status": "DENIED",
            "message": "Action cancelled by human",
        }

    return {
        "status": "RESUMED",
        "decision": decision,
    }
