# Mock Gmail tool (no real API)
from typing import Dict, List
def fetch_emails() -> List[Dict]:
    """Mock function - returns sample emails"""
    return [
        {
            "id": "mock_001",
            "sender": "alice@example.com",
            "subject": "Meeting Request",
            "body": "Can we meet next Tuesday at 2 PM?",
            "date": "2026-01-23"
        },
        {
            "id": "mock_002",
            "sender": "bob@example.com",
            "subject": "Project Update",
            "body": "Here's the latest update on our project.",
            "date": "2026-01-23"
        }
    ]
def send_reply(to: str, subject: str, body: str) -> bool:
    """Mock function - simulates sending email"""
    print(f"✅ [MOCK] Email sent to {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    return True
def mark_as_processed(email_id: str) -> bool:
    """Mock function - marks email as read"""
    print(f"✅ [MOCK] Marked email {email_id} as read")
    return True