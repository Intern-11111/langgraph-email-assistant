import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import base64
from email.mime.text import MIMEText
from typing import Optional, Tuple
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource
from googleapiclient.discovery import build
from dotenv import load_dotenv

from tools.auth import get_services 

load_dotenv()

SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials/credentials.json'
TOKEN_FILE = 'credentials/token.json'

def get_gmail_service() -> Resource:
    gmail_service, _ = get_services()
    return gmail_service
    
def get_clean_body(payload: dict) -> Optional[str]:
    """Extract plain text body from Gmail message payload."""
    if 'parts' not in payload:
        if payload.get('mimeType') == 'text/plain':
            data = payload['body'].get('data')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8')
    else:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8')
    return None

def get_sender_and_subject(full_msg: dict) -> Tuple[Optional[str], Optional[str]]:
    """Extract sender and subject from headers."""
    headers = full_msg['payload']['headers']
    sender = next((h['value'] for h in headers if h['name'] == 'From'), None)
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
    return sender, subject


def send_reply(to_email: str, subject: str, message_text: str) -> bool:
    """Send reply email. Use as @tool."""
    service = get_gmail_service()
    try:
        message = MIMEText(message_text)
        message['to'] = to_email
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw_message}
        sent_message = service.users().messages().send(userId='me', body=body).execute()
        print(f'Reply sent to {to_email} ID: {sent_message["id"]}')
        return True
    except Exception as e:
        print(f'Could not send reply: {e}')
        return False

def mark_as_processed(msg_id: str) -> bool:
    """Remove UNREAD label. Use as @tool."""
    service = get_gmail_service()
    try:
        body = {'removeLabelIds': ['UNREAD']}
        service.users().messages().modify(userId='me', id=msg_id, body=body).execute()
        print(f'Email {msg_id} marked as PROCESSED.')
        return True
    except Exception as e:
        print(f'Could not modify label: {e}')
        return False

def fetch_emails(query: str = 'in:inbox is:unread -category:social -category:promotions -category:updates -category:forums') -> list:
    """Fetch PRIMARY inbox unread emails only (read-only safe)."""
    service = get_gmail_service()
    results = service.users().messages().list(
        userId='me', 
        q=query,  
        maxResults=10
    ).execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages:
        full_msg = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        sender, subject = get_sender_and_subject(full_msg)
        body = get_clean_body(full_msg['payload']) or "No plain text"
        emails.append({
            'id': msg['id'], 
            'subject': subject, 
            'sender': sender, 
            'body': body[:500] + '...' if len(body) > 500 else body  # Truncate
        })
    return emails
