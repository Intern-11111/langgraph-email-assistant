# milestone_4_tool_interrupt/tools.py

def send_email_tool(state):
    """
    Unsafe tool: sending real email
    """
    print("📧 Sending email to recipient...")
    state["tool_result"] = "Email sent successfully"
    return state
