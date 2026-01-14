from langchain_core.tools import tool

@tool
def lookup_contact(name: str) -> dict:
    """
    Looks up contact details (email, role) for a specific person by name.

    NOTE:
    This tool accesses potentially sensitive personal information
    (email addresses) and should be treated as a READ-ONLY sensitive tool.
    """
    print(f"[Tool Log] Looking up contact info for: {name}")

    # Mock database
    contacts_db = {
        "Alice": {
            "email": "alice@company.com",
            "role": "Project Manager"
        },
        "Bob": {
            "email": "bob@client.com",
            "role": "External Client"
        },
    }

    return contacts_db.get(
        name,
        {"error": "Contact not found"}
    )
