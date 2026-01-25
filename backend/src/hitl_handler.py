from typing import Literal, Dict, Any
from langchain_core.messages import HumanMessage
from backend.src.state import AgentState

Decision = Literal["approve", "deny", "edit"]

def handle_hitl(
    app,
    config: Dict[str, Any],
    decision: Decision,
    edit_values: Dict[str, Any] | None = None,
) -> None:
    """
    Apply a human decision to the HITL envelope in the graph state.

    - app: compiled LangGraph app (from create_graph())
    - config: same config used for invoke (must include thread_id)
    - decision: "approve" | "deny" | "edit"
    - edit_values: optional overrides for hitl['args'] (for "edit")
    """
    state = app.get_state(config)
    data: AgentState = state.values  # type: ignore
    hitl = data.get("hitl") or {}
    tool_name = hitl.get("tool")
    tool_args = hitl.get("args") or {}

    if not tool_name:
        print("⚠️ No HITL envelope found; nothing to handle.")
        return

    if decision == "deny":
        #print("👤 HITL: DENY")
        denial_msg = HumanMessage(
            content="Human denied this action. Do not execute the tool."
        )
        app.update_state(
            config,
            {
                "hitl_decision": "deny",
                "messages": [denial_msg],
            },
        )
        return

    if decision == "edit":
        #print("👤 HITL: EDIT")
        edit_values = edit_values or {}
        new_args = {**tool_args, **edit_values}
        new_hitl = {**hitl, "args": new_args}
        app.update_state(
            config,
            {
                "hitl_decision": "edit",
                "hitl": new_hitl,
            },
        )
        return

    if decision == "approve":
        #print("👤 HITL: APPROVE")
        app.update_state(
            config,
            {
                "hitl_decision": "approve",
            },
        )
        return

    print("⚠️ Unknown HITL decision:", decision)
