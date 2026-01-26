from typing import Dict, List
from langchain_core.tools import tool


@tool
def read_calendar() -> List[Dict]:
    """
    Get the list of scheduled calendar events.
    This is a mock version that returns fake data for testing.
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


@tool
def send_mail(to: str, subject: str, body: str) -> Dict:
    """
    Send an email to someone.
    This is a mock version that just logs the message instead of actually sending it.
    
    Args:
        to: Email recipient address
        subject: Email subject line
        body: Email body content
    """
    print(f"[MOCK] Email sent:")
    print(f"   To: {to}")
    print(f"   Subject: {subject}")
    print(f"   Body: {body[:50]}...")
    
    return {
        "status": "sent",
        "to": to,
        "subject": subject,
        "message": "Email sent successfully (mock)"
    }

AVAILABLE_TOOLS = {
    "read_calendar": read_calendar,
    "send_mail": send_mail
}