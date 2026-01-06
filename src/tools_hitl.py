from langchain_core.tools import tool

# ---------------- SAFE TOOLS ---------------- #

@tool
def read_email():
    """Safe tool: reads email content"""
    return "Email read successfully."

@tool
def read_calendar():
    """Safe tool: reads calendar"""
    return "Calendar availability fetched."

# -------------- DANGEROUS TOOLS -------------- #

@tool
def send_email(content: str):
    """Dangerous tool: sends an email"""
    return f"Email sent: {content}"

@tool
def create_calendar_invite(details: str):
    """Dangerous tool: creates calendar invite"""
    return f"Invite created: {details}"
