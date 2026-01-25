# Simplified Tools - Only read_calendar and send_mail
# Based on Milestone 4 Task Assignment

from typing import Dict, List

# Mock Tools from team members
def read_calendar() -> List[Dict]:
    """
    Read calendar events (Samruddhi M1 - Mock Calendar Tool)
    Returns list of scheduled events
    """
    events = [
        {
            "time": "09:00 AM",
            "title": "Daily Standup",
            "attendees": ["team@example.com"]
        },
        {
            "time": "02:00 PM",
            "title": "Client Sync",
            "attendees": ["client@example.com"]
        }
    ]
    print(f"✅ [MOCK] Retrieved {len(events)} calendar events")
    return events


def send_mail(to: str, subject: str, body: str) -> Dict:
    """
    Send email (Mock Tool - Payal M4 HITL)
    Simulates sending an email
    """
    print(f"✅ [MOCK] Email sent:")
    print(f"   To: {to}")
    print(f"   Subject: {subject}")
    print(f"   Body: {body[:50]}...")
    
    return {
        "status": "sent",
        "to": to,
        "subject": subject,
        "message": "Email sent successfully (mock)"
    }


# Tool registry for agent
AVAILABLE_TOOLS = {
    "read_calendar": read_calendar,
    "send_mail": send_mail
}