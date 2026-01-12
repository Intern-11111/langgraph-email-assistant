from db import update_email

# -------------------------
# TOOL CLASSIFICATION
# -------------------------

DANGEROUS_TOOLS = {
    "reply",
    "send_email",
    "delete_email",
    "create_calendar_event",
    "reschedule_calendar_event",
}

# -------------------------
# TOOL EXECUTORS
# -------------------------

def execute_tool(action: str, action_input: dict, state: dict):
    """
    Executes the actual tool logic.
    """
    if action == "reply":
        return {
            "sent_message": action_input.get("message", "replyed")
        }

    if action == "send_email":
        return {
            "email_sent": True,
            "message": action_input.get("message", "Email sended")
    }
    if action == "delete_email":
        return {"deleted": True}

    if action == "create_calendar_event":
        return {"event_created": True}
    
    if action == "lookup_contact":
        return {
            "contact": {
                "name": action_input.get("name", "John Doe"),
                "email": "john.doe@example.com"
            }
        }

    if action == "read_calendar":
        return {
                "availability": "Available at 5 PM"
            }


    return {"status": "No tool executed"}


# -------------------------
# TOOL NODE
# -------------------------

class ToolExecutorNode:
    def __call__(self, state: dict) -> dict:
        decision = state["reasoning"][0]
        action = decision.get("action")
        action_input = decision.get("action_input")

        if not action:
            state["tool_result"] = None
            return state
        
        action = action.lower().strip()

        # HITL INTERRUPT 
        if action in DANGEROUS_TOOLS and not state.get("human_decision"):
            state["hitl"] = {
                "status": "WAITING_FOR_HUMAN",
                "email_id": state["email_id"],
                "action": action,
                "action_input": action_input,
            }
            return state

        # HANDLE HUMAN DECISION 
        if action in DANGEROUS_TOOLS:
            human_action = state["human_decision"]["action"]

            if human_action == "deny":
                update_email(state["email_id"], status="DENIED")
                state["tool_result"] = "Denied by human"
                return state

            if human_action == "edit":
                action_input = state["human_decision"]["edited_args"]
                update_email(
                    state["email_id"],
                    edited_body=str(action_input),
                    status="EDITED"
                )

            if human_action == "approve":
                update_email(
                    state["email_id"],
                    edited_body=str(action_input),
                    status="APPROVED"
                )

        # EXECUTE TOOL (AFTER APPROVAL OR SAFE TOOL)
        result = execute_tool(action, action_input, state)
        state["tool_result"] = result

        return state
