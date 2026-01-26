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
    # Support both 'tool' (old) and 'action' (new) keys
    tool_name = hitl.get("tool") or hitl.get("action")
    tool_args = hitl.get("args") or {}

    if not tool_name:
        print("⚠️ No HITL envelope found; nothing to handle.")
        return

    if decision == "deny":
        #print("👤 HITL: DENY")
        # No message history to update in template mode
        app.update_state(
            config,
            {
                "hitl_decision": "deny",
            },
        )
        return

    if decision == "edit":
        #print("👤 HITL: EDIT")
        edit_values = edit_values or {}
        new_args = {**tool_args, **edit_values}
        new_hitl = {**hitl, "args": new_args}
        
        # Determine updates to state
        updates = {
            "hitl_decision": "edit",
            "hitl": new_hitl,
            "action_args": new_args # Also update action_args
        }
        
        # If body was edited, update final_reply so the correct text is sent
        if "body" in edit_values:
            updates["final_reply"] = edit_values["body"]
            
        app.update_state(
            config,
            updates,
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
