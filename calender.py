from langchain_core.tools import tool

@tool
def read_calendar(date: str = "today") -> list:
    """
    Reads the user's calendar for a specific date or range.

    NOTE:
    This is a READ-ONLY sensitive tool.
    It accesses private schedule and participant information,
    but does not cause side effects.
    """
    print(f"[Tool Log] Accessing calendar for: {date}")

    # Mock data (replace with real calendar API in production)
    mock_events = [
        {
            "time": "09:00 AM",
            "event": "Daily Standup",
            "participants": ["team@company.com"],
        },
        {
            "time": "02:00 PM",
            "event": "Client Sync",
            "participants": ["client@external.com"],
        },
    ]

    return mock_events
