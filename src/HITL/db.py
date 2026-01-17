import json
import os
from datetime import datetime

DB_FILE = "emails.jsonl"


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_all_emails():
    if not os.path.exists(DB_FILE):
        return []

    emails = []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            emails.append(json.loads(line))  
    return emails

def save_email(subject, body):
    emails = read_all_emails()
    email_id = len(emails) + 1

    email = {
        "id": email_id,
        "subject": subject,
        "body": body,
        "agent_draft": None,
        "edited_body": None,
        "status": "CREATED",
        "created_at": _now(),
        "updated_at": _now(),
        "history": [
            {"event": "EMAIL_CREATED"}
        ],
    }

    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(email) + "\n")

    return email_id


def update_email(email_id, *, status=None, agent_draft=None,
                 edited_body=None, tool_result=None, event=None):

    emails = read_all_emails()

    for email in emails:
        if email["id"] == email_id:

            if status and email["status"] != status:
                email["status"] = status
                email["history"].append({
                    "event": "STATUS_CHANGE",
                    "value": status
                })

            if agent_draft is not None:
                email["agent_draft"] = agent_draft

            if edited_body is not None:
                email["edited_body"] = edited_body

            if tool_result is not None:
                email["history"].append({
                    "event": "TOOL_EXECUTED"
                })

            if event:
                email["history"].append(event)

            email["updated_at"] = _now()
            break

    with open(DB_FILE, "w", encoding="utf-8") as f:
        for email in emails:
            f.write(json.dumps(email) + "\n")
