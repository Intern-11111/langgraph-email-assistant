# Tools that FAIL the Undo Test (irreversible, change reality)
DANGEROUS_TOOLS = {
    "send_email",
    "create_calendar_invite",
    "spend_money",
    "delete_file",
    "update_database",
}

# Tools that PASS the Undo Test (read-only, reversible)
SAFE_TOOLS = {
    "read_email",
    "read_calendar",
    "check_weather",
    "read_file",
    "list_tasks",
}

def is_dangerous_tool(tool_name: str) -> bool:
    """
    Returns True if the tool changes reality and cannot be undone.
    """
    return tool_name in DANGEROUS_TOOLS


def is_safe_tool(tool_name: str) -> bool:
    """
    Returns True if the tool is read-only or reversible.
    """
    return tool_name in SAFE_TOOLS
