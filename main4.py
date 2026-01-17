from src.HITL.hitl_graph import build_graph
from src.HITL.db import save_email


def ask_human_decision(hitl):
    """
    Terminal-based HITL
    """
    print("\n HUMAN APPROVAL REQUIRED")
    print("Action :", hitl["action"])
    print("Draft  :", hitl["action_input"])

    choice = input("\nApprove / Edit / Deny ? (a/e/d): ").strip().lower()

    if choice == "d":
        return {"action": "deny"}

    if choice == "e":
        edited = input("\n Enter edited message:\n")
        return {
            "action": "edit",
            "edited_args": {"message": edited}
        }

    return {"action": "approve"}


def run_email(subject: str, body: str):
    print("\n==============================")
    print("New Email")
    print("==============================")
    print("Subject:", subject)
    print("Body:", body)

    email_id = save_email(subject, body)
    thread_id = f"email-{email_id}"

    graph = build_graph()

    state = {
        "email_id": email_id,
        "email_text": {
            "subject": subject,
            "body": body,
        }
    }


    result = graph.invoke(
        state,
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    # ⏸ HITL PAUSE 
    if result.get("hitl"):
        human_decision = ask_human_decision(result["hitl"])

        # RESUME WITH SAME THREAD ID
        result = graph.invoke(
            {
                **result,
                "human_decision": human_decision
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )

    print("\n==============================")
    print("🛠 TOOL RESULT")
    print("==============================")
    print(result.get("tool_result"))

    print("\n==============================")
    print("FINAL STATE")
    print("==============================")
    print(result)
    print("==============================\n")


if __name__ == "__main__":

    # Dangerous tool → HITL pause
    run_email(
        subject="Reply to manager",
        body="Reply and confirm that the meeting is scheduled for today at 5 PM."
    )

    # Dangerous tool → HITL pause
    run_email(
        subject="Send confirmation",
        body="Send an email to abc@gmail.com confirming that the task is completed."
    )

    # Safe tool → no HITL
    run_email(
        subject="Check calendar",
        body="Do I have any meetings today?"
    )

    # Notify human → no tool
    run_email(
        subject="Follow up",
        body="Do what we discussed earlier."
    )

    # Ignore
    run_email(
        subject="Limited Time Offer!",
        body="Get 50% off today only"
    )
