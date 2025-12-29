# from imapclient import IMAPClient
# import email

# def fetch_unread_emails(email_id, password, limit=5):
#     emails = []

#     with IMAPClient("imap.gmail.com") as server:
#         print("📡 Connecting to Gmail IMAP...")
#         server.login(email_id, password)
#         print("✅ Logged in")

#         server.select_folder("INBOX")
#         print("📥 Checking unread emails...")

#         messages = server.search(["UNSEEN"])
#         print(f"📨 Total unread emails: {len(messages)}")

#         # 👉 Take only the latest `limit` emails
#         latest_messages = messages[-limit:]

#         print(f"📌 Processing latest {len(latest_messages)} emails")

#         for uid in latest_messages:
#             raw = server.fetch(uid, ["RFC822"])[uid][b"RFC822"]
#             msg = email.message_from_bytes(raw)

#             subject = msg.get("Subject", "")
# sender = msg.get("From", "")

# body = ""

# if msg.is_multipart():
#     for part in msg.walk():
#         if part.get_content_type() == "text/plain":
#             body += part.get_payload(decode=True).decode(errors="ignore")
# else:
#     body = msg.get_payload(decode=True).decode(errors="ignore")

# full_email = f"""
# From: {sender}
# Subject: {subject}

# {body}
# """

# emails.append(full_email)

from imapclient import IMAPClient
import email

def fetch_unread_emails(email_id, password, limit=5):
    emails = []

    with IMAPClient("imap.gmail.com") as server:
        print("📡 Connecting to Gmail IMAP...")
        server.login(email_id, password)
        print("✅ Logged in")

        server.select_folder("INBOX")
        print("📥 Checking unread emails...")

        messages = server.search(["UNSEEN"])
        print(f"📨 Total unread emails: {len(messages)}")

        # Take only the latest `limit` unread emails
        latest_messages = messages[-limit:]
        print(f"📌 Processing latest {len(latest_messages)} emails")

        for uid in latest_messages:
            raw = server.fetch(uid, ["RFC822"])[uid][b"RFC822"]
            msg = email.message_from_bytes(raw)

            subject = msg.get("Subject", "")
            sender = msg.get("From", "")

            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body += part.get_payload(decode=True).decode(errors="ignore")
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            full_email = f"""
From: {sender}
Subject: {subject}

{body}
"""
            emails.append(full_email)

    return emails
