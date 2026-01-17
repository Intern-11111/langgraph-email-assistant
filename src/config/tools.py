# Tool Registry & Safety Classification (Milestone 4)

# Tools that FAIL the Undo Test
# (irreversible actions that change real-world state)
DANGEROUS_TOOLS = {
    "send_email",
    "create_calendar_event",
    "create_calendar_invite",
    "spend_money",
    "delete_file",
    "update_database",
}

# Tools that PASS the Undo Test
# (read-only or reversible actions)
SAFE_TOOLS = {
    "read_email",
    "read_calendar",
    "summarize",
    "check_weather",
    "read_file",
    "list_tasks",
}

# Tools that MUST be rate-limited (external APIs / quotas)
RATE_LIMITED_TOOLS = {
    "send_email",
    "create_calendar_event",
}


def is_dangerous_tool(tool_name: str) -> bool:
    """
    Returns True if the tool changes reality and cannot be undone.
    Used to trigger HITL checkpoints.
    """
    if tool_name in DANGEROUS_TOOLS:
        print(f"⚠️  Dangerous tool detected → {tool_name}")
        return True
    return False


def is_safe_tool(tool_name: str) -> bool:
    """
    Returns True if the tool is read-only or reversible.
    Safe tools never trigger HITL.
    """
    return tool_name in SAFE_TOOLS


def requires_rate_limit(tool_name: str) -> bool:
    """
    Returns True if the tool must be rate-limited
    (Gmail / Calendar / paid APIs).
    """
    return tool_name in RATE_LIMITED_TOOLS
