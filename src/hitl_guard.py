from langgraph.types import interrupt

DANGEROUS_TOOLS = ["send_email", "create_calendar_invite"]

def check_hitl(tool_name: str, tool_input: str):
    if tool_name in DANGEROUS_TOOLS:
        interrupt(
            {
                "reason": "Dangerous tool detected",
                "tool": tool_name,
                "input": tool_input,
                "action_required": "Human approval needed"
            }
        )
