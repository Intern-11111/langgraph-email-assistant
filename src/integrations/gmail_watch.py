from googleapiclient.discovery import build
from src.integrations.auth import get_google_credentials

PROJECT_ID = "langgraph-email-agent-484107"
TOPIC_NAME = "gmail-inbox"

def start_gmail_watch():
    creds = get_google_credentials()
    service = build("gmail", "v1", credentials=creds)

    request = {
        "labelIds": ["INBOX"],
        "topicName": f"projects/{PROJECT_ID}/topics/{TOPIC_NAME}",
    }

    response = service.users().watch(
        userId="me",
        body=request
    ).execute()

    print("Gmail watch started")
    print("History ID:", response.get("historyId"))
    return response
