from typing import Dict, Any

MOCK_CONTACTS = {
    "alice": {"name": "Alice Rao", "email": "alice@company.com", "phone": "+91-90000-11111"},
    "bob": {"name": "Bob Singh", "email": "bob@company.com", "phone": "+91-90000-22222"},
    "manager@company.com": {"name": "Team Manager", "email": "manager@company.com", "phone": "+91-90000-99999"},
}


def lookup_contact(query: str) -> Dict[str, Any]:
    """
    Lookup a contact by name or email (simple mock).

    Args:
        query: name or email string

    Returns:
        dict with contact details or a not-found message
    """
    q = query.strip().lower()
    if q in MOCK_CONTACTS:
        found = MOCK_CONTACTS[q]
        return {
            "tool": "lookup_contact",
            "query": query,
            "found": True,
            "contact": found,
        }

    # Try basic name match
    for key, info in MOCK_CONTACTS.items():
        if q in key or q in info["name"].lower() or q in info["email"].lower():
            return {"tool": "lookup_contact", "query": query, "found": True, "contact": info}

    return {
        "tool": "lookup_contact",
        "query": query,
        "found": False,
        "message": "No contact found in mock contacts",
    }


if __name__ == "__main__":
    print("Sample contact lookup:")
    print(lookup_contact("alice"))
