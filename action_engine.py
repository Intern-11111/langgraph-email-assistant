from gmail_auth import get_gmail_service
from review_queue import save_for_review
from review_queue import add_to_review_queue



def archive_email(msg_id):
    service = get_gmail_service()
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"removeLabelIds": ["INBOX"]}
    ).execute()

    print("✅ Email archived from INBOX")


def process_dangerous(msg_id, content, subject=None, sender=None):
    # Save full body content plus optional metadata for human review
    entry = {
        "id": msg_id,
        "content": content,
        "status": "pending",
    }
    if subject is not None:
        entry["subject"] = subject
    if sender is not None:
        entry["sender"] = sender

    save_for_review(entry)

    print("⚠ Dangerous email queued for human review")
    archive_email(msg_id)
def process_spam(msg_id):
    archive_email(msg_id)
    print("🗑️ Spam email archived")
def process_safe(msg_id):
    print("✅ Email marked as safe; no action taken")
def process_email(msg_id, classification, content, subject=None, sender=None):
    if classification == "dangerous":
        process_dangerous(msg_id, content, subject=subject, sender=sender)
    elif classification == "spam":
        process_spam(msg_id)
    else:
        process_safe(msg_id)
    