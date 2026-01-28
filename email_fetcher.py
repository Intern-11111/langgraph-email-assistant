import base64
from typing import Optional

from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

from gmail_auth import get_gmail_service


def _get_message(service, msg_id: str):
    return service.users().messages().get(userId="me", id=msg_id, format="full").execute()


def fetch_email(msg_id: str) -> Optional[str]:
    """Return Gmail snippet for the given message id."""
    service = get_gmail_service()
    try:
        res = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
        return res.get("snippet")
    except HttpError:
        return None


def fetch_email_subject(msg_id: str) -> Optional[str]:
    service = get_gmail_service()
    try:
        res = service.users().messages().get(userId="me", id=msg_id, format="metadata", metadataHeaders=["Subject"]).execute()
        headers = res.get("payload", {}).get("headers", [])
        for h in headers:
            if h.get("name") == "Subject":
                return h.get("value")
        return None
    except HttpError:
        return None


def fetch_email_sender(msg_id: str) -> Optional[str]:
    service = get_gmail_service()
    try:
        res = service.users().messages().get(userId="me", id=msg_id, format="metadata", metadataHeaders=["From"]).execute()
        headers = res.get("payload", {}).get("headers", [])
        for h in headers:
            if h.get("name") == "From":
                return h.get("value")
        return None
    except HttpError:
        return None


def _decode_part_body(body_data: str) -> str:
    try:
        # Gmail uses web-safe base64
        return base64.urlsafe_b64decode(body_data.encode("utf-8")).decode("utf-8", errors="ignore")
    except Exception:
        return ""


def fetch_email_body(msg_id: str) -> Optional[str]:
    service = get_gmail_service()
    try:
        res = _get_message(service, msg_id)
        payload = res.get("payload", {})

        # Try plain text first
        if "parts" in payload:
            for part in payload["parts"]:
                mime = part.get("mimeType", "")
                body_data = part.get("body", {}).get("data")
                if body_data and mime == "text/plain":
                    return _decode_part_body(body_data)
            # Fallback to HTML
            for part in payload["parts"]:
                mime = part.get("mimeType", "")
                body_data = part.get("body", {}).get("data")
                if body_data and mime == "text/html":
                    return _decode_part_body(body_data)
        else:
            # Single-part message
            body_data = payload.get("body", {}).get("data")
            if body_data:
                return _decode_part_body(body_data)
        return None
    except HttpError:
        return None
