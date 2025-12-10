# tools/calendar.py

def read_calendar(date=None):
    """
    Mock function that returns sample calendar events.
    """

    mock_events = [
        {"time": "10:00 AM", "event": "Team Meeting"},
        {"time": "1:00 PM", "event": "Lunch Break"},
        {"time": "4:00 PM", "event": "Project Review"}
    ]

    return {
        "status": "success",
        "events": mock_events,
        "date": date if date else "Today"
    }
