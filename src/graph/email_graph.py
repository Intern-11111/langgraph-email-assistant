from langgraph.graph import StateGraph

from src.graph.state import EmailState
from src.triage.triage_node import triage_email
from src.agents.react_loop import react_node
# from src.graph.checkpoint import checkpointer
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from src.utils.time import USER_TZ
from src.utils.logger import log

# Real integrations
from src.integrations.calendar import (
    read_calendar_availability,
    create_calendar_event,
)
from src.integrations.gmail import send_email


# --------------------------------------------------
# SAFE TOOL NODE (Undo Test PASS)
# --------------------------------------------------
def safe_tool_node(state: EmailState) -> EmailState:
    """
    SAFE tool execution node.
    Only read-only or reversible operations allowed here.
    """

    # --------------------------------------------------
    # Resume path (after HITL)
    # --------------------------------------------------
    if state.human_decision is not None:
        log(state, "SAFE TOOL SKIPPED (resuming after HITL)")
        return state

    log(state, "SAFE TOOL NODE ENTERED")
    log(state, f"CURRENT TOOL: {state.selected_tool}")

    # --------------------------------------------------
    # EMAIL-ONLY FLOW (NO CALENDAR PAYLOAD)
    # --------------------------------------------------
    if state.selected_tool == "send_email":
        log(state, "EMAIL FLOW → HITL REQUIRED")

        state.hitl_required = True
        log(state, "⏸ HITL REQUIRED — pausing before sending email")

        return state   # MUST RETURN FOR CHECKPOINT

    # --------------------------------------------------
    # CALENDAR READ FLOW
    # --------------------------------------------------
    if state.selected_tool != "read_calendar":
        log(state, "NO SAFE TOOL ACTION REQUIRED")
        return state

    log(state, "CHECKING CALENDAR AVAILABILITY")

    # ---- Defensive payload check ----
    if not state.tool_payload.get("start_time") or not state.tool_payload.get("end_time"):
        log(state, "ERROR: Missing calendar time payload")
        state.selected_tool = "send_email"
        state.hitl_required = True
        return state

    start_dt = datetime.fromisoformat(state.tool_payload["start_time"])
    end_dt = datetime.fromisoformat(state.tool_payload["end_time"])

    candidate_slots = [
        (start_dt, end_dt),
        (start_dt + timedelta(hours=1), end_dt + timedelta(hours=1)),
        (start_dt + timedelta(hours=2), end_dt + timedelta(hours=2)),
    ]

    available_slot = None

    for s, e in candidate_slots:
        try:
            is_free = read_calendar_availability(
                start_time=s.isoformat(),
                end_time=e.isoformat(),
            )
            if is_free:
                available_slot = (s, e)
                break
        except Exception as ex:
            log(state, f"CALENDAR CHECK FAILED: {str(ex)}")

    # --------------------------------------------------
    # Decision
    # --------------------------------------------------
    if available_slot:
        log(state, "AVAILABLE SLOT FOUND → PREPARE CALENDAR EVENT (dangerous)")

        state.selected_tool = "create_calendar_event"
        state.tool_payload["start_time"] = available_slot[0].isoformat()
        state.tool_payload["end_time"] = available_slot[1].isoformat()
        state.tool_payload["description"] = state.draft_reply

        state.hitl_required = True
        log(state, "⏸ HITL REQUIRED — pausing before calendar creation")

        return state   # CHECKPOINT HERE

    else:
        log(state, "NO AVAILABLE SLOTS → PREPARE EMAIL RESPONSE")

        state.selected_tool = "send_email"
        state.tool_payload = {
            "to": state.tool_payload.get("to", "recipient@example.com"),
            "subject": state.tool_payload.get("subject", "Re: Meeting"),
            "body": (
                "I’m unavailable at the proposed time. "
                "Would a later time today work for you?"
            ),
        }

        state.draft_reply = state.tool_payload["body"]
        state.hitl_required = True

        log(state, "⏸ HITL REQUIRED — pausing before sending email")

        return state   # CHECKPOINT HERE




# --------------------------------------------------
# HITL GATE NODE
# --------------------------------------------------
def hitl_gate_node(state: EmailState) -> EmailState:
    print("\nHITL GATE NODE ENTERED")
    print("HITL_REQUIRED:", state.hitl_required)
    print("HUMAN_DECISION:", state.human_decision)
    print("NEXT TOOL:", state.selected_tool)

    if state.hitl_required and state.human_decision is None:
        print("⏸ BLOCKED: Awaiting human decision")
        return state

    state.hitl_required = False
    return state



# --------------------------------------------------
# ACTION NODE (Undo Test FAIL)
# --------------------------------------------------

def action_node(state: EmailState) -> EmailState:
    """
    DANGEROUS node.
    Executes irreversible real-world actions.
    """

    print("\nACTION NODE ENTERED")
    print("DECISION:", state.human_decision)
    print("TOOL:", state.selected_tool)

    if state.human_decision is None:
        print("BLOCKED: No human decision")
        return state

    if state.human_decision == "deny":
        print("ACTION CANCELLED BY HUMAN")
        return state

    final_body = (
        state.edited_reply
        if state.human_decision == "edit"
        else state.draft_reply
    )

    try:
        if state.selected_tool == "send_email":
            print("EXECUTING: send_email()")
            send_email(
                to=state.tool_payload.get("to", "recipient@example.com"),
                subject=state.tool_payload.get(
                    "subject", "Re: Your email"
                ),
                body=final_body,
            )
            state.action_executed = True
            print("EMAIL SENT SUCCESSFULLY")

        elif state.selected_tool == "create_calendar_event":
            print("EXECUTING: create_calendar_event()")
            create_calendar_event(
                title=state.tool_payload.get("title", "Meeting"),
                start_time=state.tool_payload["start_time"],
                end_time=state.tool_payload["end_time"],
                description=final_body,
            )
            state.action_executed = True
            print("CALENDAR EVENT CREATED")

        else:
            print("UNKNOWN TOOL — NO ACTION TAKEN")

    except Exception as e:
        print("ACTION FAILED:", str(e))
        state.action_error = str(e)

    return state


# --------------------------------------------------
# GRAPH BUILDER
# --------------------------------------------------

def build_graph(checkpointer):
    graph = StateGraph(EmailState)

    graph.add_node("triage", triage_email)
    graph.add_node("react", react_node)
    graph.add_node("safe_tool", safe_tool_node)
    graph.add_node("hitl_gate", hitl_gate_node)
    graph.add_node("action_node", action_node)

    graph.set_entry_point("triage")

    graph.add_edge("triage", "react")
    graph.add_edge("react", "safe_tool")
    graph.add_edge("safe_tool", "hitl_gate")
    graph.add_edge("hitl_gate", "action_node")

    return graph.compile(
        checkpointer=checkpointer,
        interrupt_before=["hitl_gate"],
    )

