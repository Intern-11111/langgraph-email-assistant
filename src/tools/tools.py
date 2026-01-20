import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from typing import Optional, Dict, Any
from langchain_core.tools import tool
from tools.gmail import send_reply, mark_as_processed, fetch_emails
from tools.calendar import extract_event_details_llm, is_slot_available, create_calendar_event, get_calendar_service,IST
from dateutil import parser as dateparser

DANGEROUS_TOOLS = {"send_gmail_reply", "create_calendar"}
SAFE_TOOLS = {"extract_meeting_from_email", "read_calendar_availability", "get_user_prefs", "process_email"}

@tool
def send_gmail_reply(to: str, subject: str, body: str) -> str:
    """Send email reply using Gmail API. DANGEROUS - requires HITL approval."""
    print(f"Email: Sent to {to}, Subject: {subject}")
    return "Sent" if send_reply(to, subject, body) else "Failed"

@tool  # Safe
def process_email(msg_id: str) -> str:
    """Mark Gmail message as processed (remove UNREAD label)."""
    return "Processed" if mark_as_processed(msg_id) else "Failed"

@tool  # Safe: read-only
def read_calendar_availability(start: str, end: str) -> str:
    """Check calendar slot availability. Format: 'YYYY-MM-DD HH:MM' IST. Returns 'Free: True/False, Conflict: details'."""
    service = get_calendar_service()
    start_dt = dateparser.parse(start).replace(tzinfo=IST)
    end_dt = dateparser.parse(end).replace(tzinfo=IST)
    is_free, conflict = is_slot_available(service, start_dt, end_dt)
    return f"Free: {is_free}, Conflict: {conflict or 'None'}"

@tool  # DANGEROUS: HITL-gated
def create_calendar(summary: str, start: str, end: str, location: str = "Online") -> str:
    """Create calendar event. DANGEROUS - requires HITL. Use after availability check."""
    service = get_calendar_service()
    details = {"summary": summary, "location": location}
    start_dt = dateparser.parse(start).replace(tzinfo=IST)
    end_dt = dateparser.parse(end).replace(tzinfo=IST)
    return "Created" if create_calendar_event(service, details, start_dt, end_dt) else "Failed"

@tool
def extract_meeting_from_email(subject: str, body: str) -> str:
    """Extract meeting details JSON from email text using Gemini LLM."""
    details = extract_event_details_llm(body, subject)
    return json.dumps(details) if details else "No event found"

@tool  # Add for memory
def get_user_prefs(thread_id: str | None=None) -> str:
    """Get user preferences from memory (signature, name prefs). TODO: SQLite."""
    return '{"signature": "Best, Aayush"}'