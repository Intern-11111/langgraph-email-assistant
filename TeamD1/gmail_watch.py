import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_NAME = os.getenv("PUBSUB_TOPIC")

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

# Resolve token.json relative to this script's directory for robustness
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.json")

def get_gmail_service():
    """Create Gmail API service"""

    if not os.path.exists(TOKEN_FILE):
        raise Exception("token.json not found. Run gmail_auth.py first.")

    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    service = build("gmail", "v1", credentials=creds)

    return service


def start_watch():
    """Start Gmail push notification watch"""

    service = get_gmail_service()

    topic = f"projects/{PROJECT_ID}/topics/{TOPIC_NAME}"

    request_body = {
        "labelIds": ["INBOX"],
        "topicName": topic
    }

    response = service.users().watch(
        userId="me",
        body=request_body
    ).execute()

    print("\n✅ Gmail Real-Time Watch Activated Successfully!\n")
    print("Watch Response:")
    print(json.dumps(response, indent=4))


if __name__ == "__main__":
    start_watch()
