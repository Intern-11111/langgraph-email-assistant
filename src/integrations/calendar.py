from typing import List
from datetime import datetime, timezone

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import ssl
import socket
from src.integrations.auth import get_google_credentials
from src.integrations.ratelimit import enforce_rate_limit


# --------------------------------------------------
# Calendar Client
# --------------------------------------------------

def _get_calendar_service():
    """
    Build and return an authenticated Google Calendar service.
    """
    creds = get_google_credentials()
    return build("calendar", "v3", credentials=creds)


# --------------------------------------------------
# SAFE TOOL — Undo Test PASSES
# --------------------------------------------------


def read_calendar_availability(start_time: str, end_time: str) -> bool | None:
    """
    Returns:
    - True  → slot available
    - False → slot busy
    - None  → availability unknown (network / API failure)
    """

    try:
        service = _get_calendar_service()

        # ✅ Convert times FIRST
        start = (
            datetime.fromisoformat(start_time)
            .astimezone(timezone.utc)
            .isoformat()
        )
        end = (
            datetime.fromisoformat(end_time)
            .astimezone(timezone.utc)
            .isoformat()
        )

        body = {
            "timeMin": start,
            "timeMax": end,
            "timeZone": "UTC",
            "items": [{"id": "primary"}],
        }

        response = service.freebusy().query(body=body).execute()
        busy = response["calendars"]["primary"]["busy"]

        return len(busy) == 0

    except (HttpError, ssl.SSLError, socket.error, Exception) as e:
        print("Calendar API error (SAFE):", str(e))
        return None  # ✅ CRITICAL: SAFE fallback


# --------------------------------------------------
# DANGEROUS TOOL — Undo Test FAILS
# --------------------------------------------------

def create_calendar_event(
    title: str,
    start_time: str,
    end_time: str,
    description: str = "",
    calendar_id: str = "primary",
):
    """
    DANGEROUS TOOL

    Creates a REAL calendar event.
    Must ONLY run after HITL approval.
    """

    print("\nDANGEROUS TOOL EXECUTION: create_calendar_event")

    enforce_rate_limit("create_calendar_event")

    try:
        service = _get_calendar_service()

        # FIX: normalize times BEFORE building event
        start = (
            datetime.fromisoformat(start_time)
            .astimezone(timezone.utc)
            .isoformat()
        )
        end = (
            datetime.fromisoformat(end_time)
            .astimezone(timezone.utc)
            .isoformat()
        )

        event = {
            "summary": title,
            "description": description,
            "start": {
                "dateTime": start,
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end,
                "timeZone": "UTC",
            },
        }

        created_event = (
            service.events()
            .insert(calendarId=calendar_id, body=event)
            .execute()
        )

        print("CALENDAR EVENT CREATED")
        return created_event

    except HttpError as e:
        print("Calendar API error:", e)
        raise RuntimeError("Failed to create calendar event")
