import datetime
import json
import os
from typing import Dict, Any, List


def read_calendar(user_id: str = "me", date_hint: str = None) -> Dict[str, Any]:

    now = datetime.datetime.now()
    # available slots list
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


def create_event(event: Dict[str, Any], store_path: str = "data/user_events.json") -> Dict[str, Any]:
    ts = datetime.datetime.now().isoformat()
    record = {
        "tool": "create_event",
        "timestamp": ts,
        "event": event,
    }

    try:
        os.makedirs(os.path.dirname(store_path), exist_ok=True)
        if not os.path.exists(store_path) or os.path.getsize(store_path) == 0:
            with open(store_path, "w", encoding="utf-8") as f:
                json.dump([record], f, ensure_ascii=False, indent=2)
                f.write("\n")
        else:
            with open(store_path, "r", encoding="utf-8") as f:
                raw = f.read().strip()
            try:
                data = json.loads(raw) if raw else []
                if isinstance(data, list):
                    data.append(record)
                else:
                    data = [data, record]
            except json.JSONDecodeError:
                lines = [line for line in raw.splitlines() if line.strip()]
                objs = [json.loads(line) for line in lines]
                data = objs + [record]

            with open(store_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
        return {
            "tool": "create_event",
            "stored": True,
            "record": record,
            "path": store_path,
        }
    except Exception as e:
        return {
            "tool": "create_event",
            "stored": False,
            "error": str(e),
            "event": event,
        }


if __name__ == "__main__":
    print("Sample calendar read:")
    print(read_calendar(user_id="me", date_hint="next available"))
    print("\nSample create event:")
    print(create_event({"title": "Demo", "time": datetime.datetime.now().isoformat()}))