# Mock Contacts Tool - From Samruddhi Maslage (M1 Tools)
from typing import Dict, Optional

def lookup_contact(name: str) -> Optional[Dict]:
    """
    Mock contact lookup - returns hardcoded contact information.
    No real Google Contacts API.
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
    """
    Mock function - returns all available contacts.
    """
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
