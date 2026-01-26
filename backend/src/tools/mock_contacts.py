from typing import Dict, Optional

def lookup_contact(name: str) -> Optional[Dict]:
    """
    Find contact information by name.
    This is a mock version that returns hardcoded contact info for testing.
    """
    contacts = {
        "alice": {
            "name": "Alice",
            "role": "Project Manager",
            "email": "alice@company.com"
        },
        "bob": {
            "name": "Bob", 
            "role": "Client Contact",
            "email": "bob@client.com"
        }
    }
    
    contact = contacts.get(name.lower())
    
    if contact:
        print(f"✅ [MOCK] Found contact: {contact['name']} ({contact['email']})")
        return contact
    else:
        print(f"❌ [MOCK] Contact '{name}' not found")
        return None

def get_all_contacts() -> Dict[str, Dict]:
    """Get all available contacts (simulated)."""
    return {
        "alice": {
            "name": "Alice",
            "role": "Project Manager", 
            "email": "alice@company.com"
        },
        "bob": {
            "name": "Bob",
            "role": "Client Contact",
            "email": "bob@client.com"
        }
    }
