# from triage import triage_email
# from agent import react_agent

# # Sample emails to test multiple cases
# emails = [
#     """
#     Hi,
#     Can we schedule a meeting tomorrow afternoon?
#     Thanks
#     """,
#     """
#     Hello,
#     Please send me the updated report by end of day.
#     """,
#     """
#     Hey,
#     No urgent actions needed, just FYI.
#     """
# ]

# # Map decision types to messages or functions
# actions = {
#     "ignore": lambda email: print("Email archived."),
#     "notify_human": lambda email: print("Human needs to review this email."),
#     "respond": lambda email: handle_response(email)
# }

# def handle_response(email):
#     reply, thoughts = react_agent(email)

#     print("\nAgent Thoughts:")
#     for t in thoughts:
#         print("-", t)

#     print("\nDraft Reply:")
#     print(reply)

# # Process each email
# for idx, email in enumerate(emails, 1):
#     print(f"\n{'='*20}\nEmail {idx}:\n{email.strip()}\n{'='*20}")
#     decision = triage_email(email)
#     print("Triage Decision:", decision)

#     # Call the corresponding action
#     if decision in actions:
#         actions[decision](email)
#     else:
#         print("Unknown decision. Needs review.")

# from triage import triage_email
# from agent import react_agent

# emails = [
#     """
#     Hi,
#     Can we schedule a meeting tomorrow afternoon?
#     Thanks
#     """,
#     """
#     Hello,
#     Please send me the updated report by end of day.
#     """,
#     """
#     Hey,
#     No urgent actions needed, just FYI.
#     """
# ]

# def handle_response(email):
#     reply, thoughts = react_agent(email)

#     print("\nAgent Thoughts:")
#     for t in thoughts:
#         print("-", t)

#     print("\nDraft Reply:")
#     print(reply)

# actions = {
#     "ignore": lambda email: print("Email archived."),
#     "notify_human": lambda email: print("Human needs to review this email."),
#     "respond": lambda email: handle_response(email)
# }

# for idx, email in enumerate(emails, 1):
#     print(f"\n{'='*20}")
#     print(f"Email {idx}:")
#     print(email.strip())
#     print(f"{'='*20}")

#     decision = triage_email(email)
#     print("Triage Decision:", decision)

#     if decision in actions:
#         actions[decision](email)
#     else:
#         print("Unknown decision. Needs review.")

from graph import app

# emails = [
#     """
#     Hi,
#     Can we schedule a meeting tomorrow afternoon?
#     Thanks
#     """,
#     """
#     Hello,
#     Please send me the updated report by end of day.
#     """,
#     """
#     Hey,
#     No urgent actions needed, just FYI.
#     """
# ]

# for idx, email in enumerate(emails, 1):
#     print(f"\n{'='*20}")
#     print(f"Email {idx}:")
#     print(email.strip())
#     print(f"{'='*20}")

#     result = app.invoke({
#         "email": email,
#         "category": "",
#         "thoughts": [],
#         "reply": ""
#     })

#     print("Triage Decision:", result["category"])

#     if result["category"] == "respond":
#         print("\nAgent Thoughts:")
#         for t in result["thoughts"]:
#             print("-", t)

#         print("\nDraft Reply:")
#         print(result["reply"])

#     elif result["category"] == "notify_human":
#         print("Human needs to review this email.")

#     else:
#         print("Email archived.")

from graph import app
from email_reader import fetch_unread_emails
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ID")
PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

emails = fetch_unread_emails(EMAIL, PASSWORD)

for email_text in emails:
    print("\n" + "=" * 50)
    print("📧 New Email Received")
    print("=" * 50)

    result = app.invoke({
        "email": email_text,
        "category": "",
        "thoughts": [],
        "reply": ""
    })

    print("Decision:", result["category"])

    if result["category"] == "respond":
        print("\nAgent Thoughts:")
        for t in result["thoughts"]:
            print("-", t)

        print("\nDraft Reply:")
        print(result["reply"])

    elif result["category"] == "notify_human":
        print("⚠️ Human review required.")

    else:
        print("🗑️ Email ignored.")
