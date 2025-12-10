# tools/contacts.py

CONTACTS = {
    "bob": "bob@gmail.com",
    "alice": "alice@yahoo.com",
    "john": "john@company.com"
}

def lookup_contact(name):
    name = name.lower()

    if name in CONTACTS:
        return {
            "status": "success",
            "name": name,
            "email": CONTACTS[name]
        }

    return {
        "status": "not_found",
        "message": f"No contact found for {name}"
    }
