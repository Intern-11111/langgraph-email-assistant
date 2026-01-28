def read_calendar():
    return "Calendar is free tomorrow between 3 PM - 5 PM"
# tools.py

def send_email(to: str, subject: str, body: str):
    print(f"[ACTION] Sending email to {to}")
    print(f"Subject: {subject}")
    print(body)
    return "Email sent"


def read_email():
    return "Email read"


def delete_email():
    return "Email deleted"
