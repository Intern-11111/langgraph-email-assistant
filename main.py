

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
from graph import build_graph
from email_reader import fetch_unread_emails
from langsmith import traceable
print("🔍 LANGCHAIN TRACING:", os.getenv("LANGCHAIN_TRACING_V2"))
EMAIL = os.getenv("EMAIL_ID")
PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# Build LangGraph app
app = build_graph()

# -------------------------------
# Milestone 1: Fetch Emails
# -------------------------------
emails = fetch_unread_emails(EMAIL, PASSWORD)

if not emails:
    print("📭 No unread emails found.")
else:
    for idx, email_text in enumerate(emails, start=1):
        print("\n" + "=" * 50)
        print(f"📧 New Email Received ({idx})")
        print("=" * 50)

        subject = email_text
        body = email_text

        body = email_text if email_text else ""

        result = app.invoke(
            {
                "sender": sender,
                "subject": subject,
                "body": body,
                "requires_approval": False,
                "intent": None,
                "approved": None
            },
            config={
                "configurable": {
                    "thread_id": f"email_thread_{idx}"
                }
            }
        )
        print("📌 Triage Category:", result["category"])
        print("🧠 Agent Decision:", result.get("action_taken"))
        # ✅ Decision handling MUST be inside loop
        if result.get("requires_approval"):
            print("⚠️ Human approval required.")
        else:
            print("✅ Safe email. No approval needed.")
