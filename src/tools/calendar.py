import datetime
from typing import Dict, Any, List


def read_calendar(user_id: str = "me", date_hint: str = None) -> Dict[str, Any]:

    now = datetime.datetime.now()
    # Simple deterministic "available slots" list
    base_hour = 9
    available_slots: List[str] = []
    for i in range(4):
        slot_time = (now + datetime.timedelta(days=i)).replace(hour=base_hour + i, minute=0, second=0, microsecond=0)
        available_slots.append(slot_time.isoformat())

    events = [
        {"title": "Daily Standup", "time": (now.replace(hour=10, minute=0)).isoformat()},
        {"title": "Project Sync", "time": (now.replace(hour=15, minute=0)).isoformat()},
    ]

    # If a date_hint is included, include it in returned context
    hint_text = f"Date hint received: {date_hint}" if date_hint else "No date hint"

    return {
        "tool": "read_calendar",
        "user_id": user_id,
        "available_slots": available_slots,
        "events": events,
        "note": hint_text,
    }


if __name__ == "__main__":
    print("Sample calendar read:")
    print(read_calendar(user_id="me", date_hint="next available"))
