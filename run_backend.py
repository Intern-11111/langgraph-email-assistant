from src.triage.triage_node import triage_node
from src.react_agent.reasoning import reasoning_node
from src.react_agent.approval import approval_node
from src.tools.tools import is_dangerous_tool, send_email_tool


def run_agent(subject, body, user_action=None, edited_text=None):

    state = {
        "email": {
            "subject": subject,
            "body": body
        }
    }

    # --------------------------------
    # STEP 1 — TRIAGE
    # --------------------------------
    state = triage_node(state)

    decision = state["triage_decision"]

    # --------------------------------
    # STEP 2 — IGNORE
    # --------------------------------
    if decision == "ignore":
        state["tool_status"] = "ignored"
        return state

    # --------------------------------
    # STEP 3 — DRAFT
    # --------------------------------
    state = reasoning_node(state)

    action = "send_email"

    # =============================================
    # ✅ SAFE EMAILS → AUTO SEND (NO APPROVAL)
    # =============================================
    if decision == "respond":
        state = send_email_tool(state)
        state["tool_status"] = "auto_sent"
        return state

    # =============================================
    # ⚠ NEEDS HUMAN REVIEW → HITL
    # =============================================
    if decision == "needs_human_review":

        state = approval_node(
            state,
            user_action=user_action,
            edited_text=edited_text
        )

        if state.get("approved"):
            state = send_email_tool(state)
            state["tool_status"] = "approved_sent"
        else:
            state["tool_status"] = "blocked"

        return state

    return state
