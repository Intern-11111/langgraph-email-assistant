from triage import triage_email
from agent import react_agent

# Sample emails to test multiple cases
emails = [
    """
    Hi,
    Can we schedule a meeting tomorrow afternoon?
    Thanks
    """,
    """
    Hello,
    Please send me the updated report by end of day.
    """,
    """
    Hey,
    No urgent actions needed, just FYI.
    """
]

# Map decision types to messages or functions
actions = {
    "ignore": lambda email: print("Email archived."),
    "notify_human": lambda email: print("Human needs to review this email."),
    "respond": lambda email: handle_response(email)
}

def handle_response(email):
    reply, thoughts = react_agent(email)

    print("\nAgent Thoughts:")
    for t in thoughts:
        print("-", t)

    print("\nDraft Reply:")
    print(reply)

# Process each email
for idx, email in enumerate(emails, 1):
    print(f"\n{'='*20}\nEmail {idx}:\n{email.strip()}\n{'='*20}")
    decision = triage_email(email)
    print("Triage Decision:", decision)

    # Call the corresponding action
    if decision in actions:
        actions[decision](email)
    else:
        print("Unknown decision. Needs review.")
