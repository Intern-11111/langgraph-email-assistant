from __future__ import annotations

import calendar
import datetime
import json
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Event:
    id: str
    title: str
    start: datetime.datetime
    end: Optional[datetime.datetime] = None
    description: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "start": self.start.isoformat(),
            "end": self.end.isoformat() if self.end else None,
            "description": self.description,
        }

    @staticmethod
    def from_dict(data: Dict) -> "Event":
        return Event(
            id=data["id"],
            title=data["title"],
            start=datetime.datetime.fromisoformat(data["start"]),
            end=datetime.datetime.fromisoformat(data["end"]) if data.get("end") else None,
            description=data.get("description"),
        )


class CalendarTool:
    def __init__(self) -> None:
        self.events: Dict[str, Event] = {}

    def add_event(
        self,
        title: str,
        start: datetime.datetime,
        end: Optional[datetime.datetime] = None,
        description: Optional[str] = None,
    ) -> str:
        eid = str(uuid.uuid4())
        ev = Event(id=eid, title=title, start=start, end=end, description=description)
        self.events[eid] = ev
        return eid

    def remove_event(self, event_id: str) -> bool:
        return self.events.pop(event_id, None) is not None

    def list_events(self, for_date: Optional[datetime.date] = None) -> List[Event]:
        if for_date is None:
            return list(self.events.values())
        result: List[Event] = []
        for ev in self.events.values():
            if ev.start.date() == for_date or (ev.end and ev.end.date() == for_date):
                result.append(ev)
        return sorted(result, key=lambda e: e.start)

    def events_on(self, year: int, month: int) -> Dict[int, List[Event]]:
        days: Dict[int, List[Event]] = {}
        for ev in self.events.values():
            if ev.start.year == year and ev.start.month == month:
                days.setdefault(ev.start.day, []).append(ev)
            elif ev.end and ev.end.year == year and ev.end.month == month:
                days.setdefault(ev.end.day, []).append(ev)
        return days

    def save(self, path: str | Path) -> None:
        path = Path(path)
        data = [ev.to_dict() for ev in self.events.values()]
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load(self, path: str | Path) -> None:
        path = Path(path)
        if not path.exists():
            return
        raw = json.loads(path.read_text(encoding="utf-8"))
        self.events = {d["id"]: Event.from_dict(d) for d in raw}

    def print_month(self, year: int, month: int, show_events: bool = True) -> None:
        cal = calendar.TextCalendar(firstweekday=0)
        print(cal.formatmonth(year, month))
        if show_events:
            days = self.events_on(year, month)
            if not days:
                print("No events for this month.")
                return
            for day in sorted(days):
                print(f"{year}-{month:02d}-{day:02d}:")
                for ev in sorted(days[day], key=lambda e: e.start):
                    start = ev.start.strftime("%Y-%m-%d %H:%M")
                    end = ev.end.strftime("%Y-%m-%d %H:%M") if ev.end else ""
                    print(f"  - {ev.title} ({start}{(' - ' + end) if end else ''})")


def demo() -> None:
    cal_tool = CalendarTool()
    now = datetime.datetime.now()
    cal_tool.add_event(
        title="Project sync",
        start=now.replace(hour=10, minute=0, second=0, microsecond=0),
        end=now.replace(hour=11, minute=0, second=0, microsecond=0),
        description="Weekly team sync",
    )
    cal_tool.add_event(
        title="Release prep",
        start=(now + datetime.timedelta(days=3)).replace(hour=15, minute=30),
        description="Prepare release notes",
    )
    print("Demo calendar output:\n")
    cal_tool.print_month(now.year, now.month)


if __name__ == "__main__":
    demo()

