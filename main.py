from src.tools import send_email_tool
from src.hitl import handle_hitl_decision


def classify_email(email_text):
    if "refund" in email_text.lower():
        return "dangerous"
    return "safe"


def main():
    email_text = "Customer wants a refund for recent purchase"
    print("Incoming email:", email_text)

    action_type = classify_email(email_text)
    print("Action type detected:", action_type)

    if action_type == "dangerous":
        print("HITL PAUSE: waiting for human decision")

        # simulate human decision
        user_choice = "approve"  # change to "deny" to test
        print("Human decision:", user_choice)

        result = handle_hitl_decision(
            user_choice,
            send_email_tool,
            "customer@email.com",
            "Refund Request",
            "Your refund is being processed"
        )

        print("Final result:", result)

    else:
        print("Safe action, no HITL required")


if __name__ == "__main__":
    main()
