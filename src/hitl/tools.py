def send_email(state: dict):
    # This is a SENSITIVE / DANGEROUS tool
    recipient = "client@example.com"
    subject = state["email"]["subject"]

    return {
        "tool": "send_email",
        "status": "ready",
        "message": f"Email ready to send to {recipient} with subject '{subject}'"
    }
