import json
from pathlib import Path

DB_PATH = Path("emails.jsonl")


def read_all_emails():
    if not DB_PATH.exists():
        return []

    emails = []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        for line in f:
            emails.append(json.loads(line))
    return emails


def get_email(email_id: int):
    for email in read_all_emails():
        if email["id"] == email_id:
            return email
    return None


def save_email(subject: str, body: str):
    emails = read_all_emails()
    new_id = max([e["id"] for e in emails], default=0) + 1

    record = {
        "id": new_id,
        "subject": subject,
        "body": body,
        "edited_body": None,
        "status": "PENDING"
    }

    with open(DB_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    return new_id


def update_email(email_id: int, *, edited_body=None, status=None):
    emails = read_all_emails()

    with open(DB_PATH, "w", encoding="utf-8") as f:
        for email in emails:
            if email["id"] == email_id:
                if edited_body is not None:
                    email["edited_body"] = edited_body
                if status is not None:
                    email["status"] = status

            f.write(json.dumps(email) + "\n")
