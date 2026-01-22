from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Contact:
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "notes": self.notes,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: Dict) -> "Contact":
        return Contact(
            id=data["id"],
            name=data["name"],
            email=data.get("email"),
            phone=data.get("phone"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
        )


class ContactBook:
    def __init__(self) -> None:
        self.contacts: Dict[str, Contact] = {}

    def add_contact(self, name: str, email: Optional[str] = None, phone: Optional[str] = None, notes: Optional[str] = None) -> str:
        cid = str(uuid.uuid4())
        c = Contact(id=cid, name=name, email=email, phone=phone, notes=notes)
        self.contacts[cid] = c
        return cid

    def remove_contact(self, contact_id: str) -> bool:
        return self.contacts.pop(contact_id, None) is not None

    def find_by_name(self, name_substring: str) -> List[Contact]:
        name_substring = name_substring.lower()
        return [c for c in self.contacts.values() if name_substring in c.name.lower()]

    def find_by_email(self, email: str) -> Optional[Contact]:
        for c in self.contacts.values():
            if c.email and c.email.lower() == email.lower():
                return c
        return None

    def list_contacts(self) -> List[Contact]:
        return sorted(self.contacts.values(), key=lambda c: c.name)

    def save(self, path: str | Path) -> None:
        path = Path(path)
        data = [c.to_dict() for c in self.contacts.values()]
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load(self, path: str | Path) -> None:
        path = Path(path)
        if not path.exists():
            return
        raw = json.loads(path.read_text(encoding="utf-8"))
        self.contacts = {d["id"]: Contact.from_dict(d) for d in raw}

    def pretty_print(self) -> None:
        for c in self.list_contacts():
            print(f"{c.name} <{c.email or 'no-email'}> {c.phone or ''}")
            if c.notes:
                print(f"  notes: {c.notes}")


def demo() -> None:
    cb = ContactBook()
    cb.add_contact("Alice Johnson", email="alice@example.com", phone="+1-555-0100", notes="Project manager")
    cb.add_contact("Bob Lee", email="bob@example.com", phone=None, notes="Contractor")
    cb.add_contact("Charlie", notes="Met at conference")

    print("ContactBook demo:\n")
    cb.pretty_print()

    # save and load test
    tmp = Path(__file__).with_suffix('.contacts.json')
    cb.save(tmp)
    print(f"\nSaved contacts to {tmp}")

    cb2 = ContactBook()
    cb2.load(tmp)
    print("\nReloaded contacts:\n")
    cb2.pretty_print()


if __name__ == '__main__':
    demo()
