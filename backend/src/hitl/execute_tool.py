from src.HITL.db import update_email

DANGEROUS_TOOLS = {
    "reply",
    "send_email",
    "delete_email",
    "create_calendar_event",
    "reschedule_calendar_event",
}


def execute_tool(action: str, action_input: dict):
    if action == "reply":
        return {"sent_message": action_input.get("message", "Replied successfully")}

    if action == "send_email":
        return {
            "email_sent": True,
            "message": action_input.get("message", "Email sent"),
        }

    if action == "delete_email":
        return {"deleted": True}

    if action == "create_calendar_event":
        return {"event_created": True}

    if action == "lookup_contact":
        return {
            "contact": {
                "name": action_input.get("name", "John Doe"),
                "email": "john.doe@example.com",
            }
        }

    if action == "read_calendar":
        return {"availability": "Available at 5 PM"}

    return None


class ToolExecutorNode:
    def __call__(self, state: dict) -> dict:
        decision = state["reasoning"][0]
        action = decision.get("action")
        action_input = decision.get("action_input", {})

        if not action:
            return state

        action = action.lower().strip()

        
        
        if not state.get("_agent_draft_saved"):
            update_email(
                state["email_id"],
                agent_draft={"action": action, "action_input": action_input},
            )
            state["_agent_draft_saved"] = True

        if (
            action in DANGEROUS_TOOLS
            and not state.get("_hitl_locked")
            and not state.get("human_decision")
        ):
            update_email(
                state["email_id"],
                status="WAITING_FOR_APPROVAL",
                event={"event": "HITL", "value": action},
            )

            state["_hitl_locked"] = True
            state["hitl"] = {
                "email_id": state["email_id"],
                "action": action,
                "action_input": action_input,
            }
            return state

       
       
        if action in DANGEROUS_TOOLS and state.get("human_decision"):
            decision = state["human_decision"]["action"]

            if decision == "deny":
                update_email(state["email_id"], status="DENIED")
                state["status"] = "DENIED"
                return state  
            
            if decision == "edit":
                action_input = state["human_decision"]["edited_args"]
                update_email(
                    state["email_id"],
                    edited_body=action_input,
                    status="EDITED",
                )

            if decision == "approve":
                update_email(state["email_id"], status="APPROVED")

       
        if not state.get("_tool_executed"):
            result = execute_tool(action, action_input)
            state["_tool_executed"] = True
            state["tool_result"] = result

            update_email(
                state["email_id"],
                event={"event": "TOOL_EXECUTED"},
            )

        return state
