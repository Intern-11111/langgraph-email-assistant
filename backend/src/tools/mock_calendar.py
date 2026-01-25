# Mock Calendar Tool - From Samruddhi Maslage (M1 Tools)
from typing import Dict, List, Optional

def read_calendar() -> List[Dict]:
    """
    Mock calendar function - returns hardcoded scheduled events.
    No real Google Calendar API.
    """
    return [
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

def check_availability(date: str, time: str) -> Dict[str, bool]:
    """
    Mock function - checks if a time slot is available.
    Always returns true for demonstration.
    """
    print(f"✅ [MOCK] Checking calendar for {date} at {time}")
    return {
        "available": True,
        "conflicts": []
    }

def create_calendar_event(summary: str, start: str, end: str) -> bool:
    """
    Mock function - simulates creating a calendar event.
    """
    print(f"✅ [MOCK] Calendar event created:")
    print(f"  Summary: {summary}")
    print(f"  Start: {start}")
    print(f"  End: {end}")
    return True
