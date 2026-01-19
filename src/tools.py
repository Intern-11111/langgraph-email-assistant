"""
Mock tools for Milestone 4.

These tools simulate dangerous actions.
They do not perform real-world side effects.
"""

def send_email_tool(to, subject, body):
    print("MOCK TOOL: send_email")
    print("To:", to)
    print("Subject:", subject)
    print("Body:", body)
    return "email_sent_successfully"


def create_calendar_invite_tool(date, time, participants):
    print("MOCK TOOL: create_calendar_invite")
    print("Date:", date)
    print("Time:", time)
    print("Participants:", participants)
    return "calendar_invite_created"
