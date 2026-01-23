"""
Tools + Safety Logic
"""

# Dangerous tools list
DANGEROUS_TOOLS = {"send_email"}


def is_dangerous_tool(name: str) -> bool:
    """
    Returns True if tool requires human approval
    """
    return name in DANGEROUS_TOOLS


def send_email_tool(state):
    """
    Mock email sender
    """
    state["tool_status"] = "sent"
    return state
