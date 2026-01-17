import base64
from email.mime.text import MIMEText
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.integrations.auth import get_google_credentials
from src.integrations.ratelimit import enforce_rate_limit



# Gmail Client

def _get_gmail_service():
    """
    Build and return an authenticated Gmail service
    using centralized OAuth handling.
    """
    creds = get_google_credentials()
    return build("gmail", "v1", credentials=creds)


# DANGEROUS TOOL — Undo Test FAILS

def send_email(
    to: str,
    subject: str,
    body: str,
    sender: Optional[str] = "me",
):
    """
    DANGEROUS TOOL: Sends a REAL email via Gmail API.

    Must ONLY be executed AFTER HITL approval.
    """

    if not to:
        raise ValueError("Recipient email address is required")

    print("\nDANGEROUS TOOL EXECUTION: send_email")

    # Enforce API rate limits
    enforce_rate_limit("send_email")

    try:
        service = _get_gmail_service()

        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject

        raw_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode("utf-8")

        result = (
            service.users()
            .messages()
            .send(
                userId=sender,
                body={"raw": raw_message},
            )
            .execute()
        )

        print("EMAIL SENT SUCCESSFULLY")
        return result

    except HttpError as e:
        print("Gmail API error:", e)
        raise RuntimeError("Failed to send email via Gmail API")
    
def get_header(headers, name: str) -> Optional[str]:
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value")
    return None

def extract_body(payload) -> str:
    """
    Extracts the email body from Gmail message payload.
    Handles multipart and base64 decoding safely.
    """
    if "body" in payload and payload["body"].get("data"):
        return base64.urlsafe_b64decode(
            payload["body"]["data"]
        ).decode("utf-8", errors="ignore")

    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")
            if mime_type == "text/plain" and part["body"].get("data"):
                return base64.urlsafe_b64decode(
                    part["body"]["data"]
                ).decode("utf-8", errors="ignore")

    return ""


def fetch_latest_email():
    service = _get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=1
    ).execute()

    if "messages" not in results:
        return None

    msg_id = results["messages"][0]["id"]

    msg = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="full"
    ).execute()

    headers = msg["payload"]["headers"]
    body = extract_body(msg["payload"])

    return {
        "message_id": msg_id,
        "from": get_header(headers, "From"),
        "subject": get_header(headers, "Subject"),
        "body": body,
    }

