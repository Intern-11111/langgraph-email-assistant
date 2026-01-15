# src/hitl_graph.py

from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.types import interrupt

from triage_agent import triage_email


# -----------------------------
# Graph State
# -----------------------------
class EmailState(TypedDict):
    email_body: str
    decision: str
    approved: bool | None


# -----------------------------
# Nodes
# -----------------------------
def triage_node(state: EmailState) -> EmailState:
    email = state.get("email_body", "").strip()
    raw_decision = triage_email(email)

    # ✅ SAFETY GUARD: enforce valid routing keys
    if raw_decision not in ("respond", "ignore", "notify_human"):
        decision = "ignore"   # safest fallback
    else:
        decision = raw_decision

    return {**state, "decision": decision}



def safe_action_node(state: EmailState) -> EmailState:
    # respond / ignore
    return state


def hitl_pause_node(state: EmailState) -> EmailState:
    # INTERRUPT: wait for human input
    human_input = interrupt(
        {
            "message": "This action is risky. Approve?",
            "decision": state["decision"]
        }
    )
    return {**state, "approved": human_input["approved"]}


def resume_node(state: EmailState) -> EmailState:
    # After approval
    return state


# -----------------------------
# Build Graph
# -----------------------------
def build_hitl_graph():
    graph = StateGraph(EmailState)

    graph.add_node("triage", triage_node)
    graph.add_node("safe_action", safe_action_node)
    graph.add_node("hitl_pause", hitl_pause_node)
    graph.add_node("resume", resume_node)

    graph.set_entry_point("triage")

    graph.add_conditional_edges(
        "triage",
        lambda s: s["decision"],
        {
            "respond": "safe_action",
            "ignore": "safe_action",
            "notify_human": "hitl_pause",
        },
    )

    graph.add_conditional_edges(
        "hitl_pause",
        lambda s: s["approved"],
        {
            True: "resume",
            False: END,
        },
    )

    graph.add_edge("safe_action", END)
    graph.add_edge("resume", END)

    return graph.compile()
