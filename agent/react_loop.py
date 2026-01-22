from __future__ import annotations

import asyncio
import datetime
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

STORAGE_DIR = Path(__file__).resolve().parent.parent
EVENTS_FILE = STORAGE_DIR / ".react_events.json"
CONTACTS_FILE = STORAGE_DIR / ".react_contacts.json"


@dataclass
class Event:
    id: str
    title: str
    start: str  # ISO format
    duration_minutes: Optional[int] = None
    description: Optional[str] = None


@dataclass
class Contact:
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None


class ReactiveAgent:
    def __init__(self) -> None:
        self.events: Dict[str, Event] = {}
        self.contacts: Dict[str, Contact] = {}

    def add_event(self, title: str, start_iso: str, duration_minutes: Optional[int], description: Optional[str]) -> str:
        eid = str(len(self.events) + 1)
        ev = Event(id=eid, title=title, start=start_iso, duration_minutes=duration_minutes, description=description)
        self.events[eid] = ev
        return eid

    def list_events(self, for_date: Optional[str] = None) -> List[Event]:
        if not for_date:
            return list(self.events.values())
        try:
            target = datetime.date.fromisoformat(for_date)
        except Exception:
            return []
        out = []
        for e in self.events.values():
            try:
                d = datetime.datetime.fromisoformat(e.start).date()
            except Exception:
                continue
            if d == target:
                out.append(e)
        return out

    def add_contact(self, name: str, email: Optional[str], phone: Optional[str], notes: Optional[str]) -> str:
        cid = str(len(self.contacts) + 1)
        c = Contact(id=cid, name=name, email=email, phone=phone, notes=notes)
        self.contacts[cid] = c
        return cid

    def list_contacts(self) -> List[Contact]:
        return list(self.contacts.values())

    def save(self) -> None:
        STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        EVENTS_FILE.write_text(json.dumps([asdict(e) for e in self.events.values()], indent=2), encoding="utf-8")
        CONTACTS_FILE.write_text(json.dumps([asdict(c) for c in self.contacts.values()], indent=2), encoding="utf-8")

    def load(self) -> None:
        if EVENTS_FILE.exists():
            raw = json.loads(EVENTS_FILE.read_text(encoding="utf-8"))
            self.events = {d["id"]: Event(**d) for d in raw}
        if CONTACTS_FILE.exists():
            raw = json.loads(CONTACTS_FILE.read_text(encoding="utf-8"))
            self.contacts = {d["id"]: Contact(**d) for d in raw}


async def repl(agent: ReactiveAgent) -> None:
    banner = (
        "Reactive Agent REPL\n"
        "Commands:\n"
        "  help\n"
        "  quit\n"
        "  add-event <title>|<YYYY-MM-DDTHH:MM> [|duration_minutes] [|description]\n"
        "  list-events [YYYY-MM-DD]\n"
        "  add-contact <name>|[email]|[phone]|[notes]\n"
        "  list-contacts\n"
        "  save\n"
        "  load\n"
    )
    print(banner)

    while True:
        try:
            cmd = await asyncio.to_thread(input, "agent> ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting REPL")
            break
        cmd = cmd.strip()
        if not cmd:
            continue
        parts = cmd.split(" ", 1)
        op = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if op == "help":
            print(banner)
        elif op == "quit" or op == "exit":
            print("Goodbye")
            break
        elif op == "add-event":
            # format: title|YYYY-MM-DDTHH:MM|duration_minutes|description
            fields = [s.strip() for s in arg.split("|")]
            if len(fields) < 2 or not fields[0] or not fields[1]:
                print("Usage: add-event <title>|<YYYY-MM-DDTHH:MM> [|duration_minutes] [|description]")
                continue
            title = fields[0]
            start = fields[1]
            duration = int(fields[2]) if len(fields) >= 3 and fields[2] else None
            description = fields[3] if len(fields) >= 4 and fields[3] else None
            try:
                # validate date
                _ = datetime.datetime.fromisoformat(start)
            except Exception:
                print("Invalid datetime format. Use ISO like 2025-12-29T09:30")
                continue
            eid = agent.add_event(title, start, duration, description)
            print(f"Event added id={eid}")
        elif op == "list-events":
            date = arg.strip() or None
            evs = agent.list_events(date)
            if not evs:
                print("No events")
            for e in evs:
                print(f"{e.id}: {e.title} @ {e.start} (+{e.duration_minutes or 0}m) {e.description or ''}")
        elif op == "add-contact":
            # format: name|email|phone|notes
            fields = [s.strip() for s in arg.split("|")]
            if not fields[0]:
                print("Usage: add-contact <name>|[email]|[phone]|[notes]")
                continue
            name = fields[0]
            email = fields[1] if len(fields) > 1 and fields[1] else None
            phone = fields[2] if len(fields) > 2 and fields[2] else None
            notes = fields[3] if len(fields) > 3 and fields[3] else None
            cid = agent.add_contact(name, email, phone, notes)
            print(f"Contact added id={cid}")
        elif op == "list-contacts":
            cs = agent.list_contacts()
            if not cs:
                print("No contacts")
            for c in cs:
                print(f"{c.id}: {c.name} <{c.email or 'no-email'}> {c.phone or ''}")
                if c.notes:
                    print(f"  notes: {c.notes}")
        elif op == "save":
            agent.save()
            print(f"Saved events -> {EVENTS_FILE}, contacts -> {CONTACTS_FILE}")
        elif op == "load":
            agent.load()
            print("Loaded data from storage")
        else:
            print("Unknown command. Type 'help' for list of commands.")


async def main() -> None:
    agent = ReactiveAgent()
    agent.load()
    await repl(agent)
    # auto-save before exit
    agent.save()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")

