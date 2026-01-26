from typing import Dict, List

def read_calendar() -> List[Dict]:
    """
    Get the list of scheduled calendar events.
    This is a mock version that returns fake events for testing.
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
    Check if a calendar time slot is free (simulated - always returns available).
    """
    print(f"[MOCK] Checking calendar for {date} at {time}")
    return {
        "available": True,
        "conflicts": []
    }

def create_calendar_event(summary: str, start: str, end: str) -> bool:
    """Create a new calendar event (simulated - just logs the details)."""
    print(f"[MOCK] Calendar event created:")
    print(f"  Summary: {summary}")
    print(f"  Start: {start}")
    print(f"  End: {end}")
    return True
