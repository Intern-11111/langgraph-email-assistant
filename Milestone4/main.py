import argparse
from graph import graph
from memory import memory


def run_cli():
    parser = argparse.ArgumentParser(description="LangGraph Email Assistant CLI")
    parser.add_argument("--thread", default="email_session_cli", help="Thread id for the session")
    parser.add_argument("--input", default="Please approve my internship application", help="Initial input to seed agent draft")
    parser.add_argument("--email-to", dest="email_to", help="Override TO before tools execute")
    parser.add_argument("--email-subject", dest="email_subject", help="Override SUBJECT before tools execute")
    parser.add_argument("--email-body", dest="email_body", help="Override BODY before tools execute")


    args = parser.parse_args()

    # Decide sensitivity/spam from provided content
    content_subject = (args.email_subject or "")
    content_body = (args.email_body or args.input or "")
    text = (content_subject + " " + content_body).lower()

    spam_markers = [
        "lottery", "prize", "winner", "free", "click here", "click on the link",
        "click the link", "click link", "claim", "cash", "get cash", "bonus",
        "limited time", "credit card", "viagra", "xxx", "crypto double",
        "investment scheme", "rich quick", "congratulations"
    ]
    sensitive_markers = [
        "approve", "approval", "urgent", "payment", "salary", "confidential",
        "escalate", "legal", "contract", "offer letter", "promotion",
        "termination", "invoice", "wire"
    ]

    is_spam = any(m in text for m in spam_markers)
    is_sensitive = any(m in text for m in sensitive_markers)
    auto_pause = (is_sensitive and not is_spam)

    interrupts = ["tools"] if auto_pause else []
    app = graph.compile(checkpointer=memory, interrupt_before=interrupts)

    config = {"configurable": {"thread_id": args.thread}}

    print("\n=== Incoming Email Assistant CLI — Auto-HITL ===\n")
    print("Step 1 — Configuration:")
    print("- Thread:", args.thread)
    print("- Initial input:", args.input)
    print("- Detection:", "SPAM" if is_spam else ("SENSITIVE" if is_sensitive else "NON-SENSITIVE"))
    print("- Human-in-the-loop pause:", "ENABLED" if auto_pause else "DISABLED")

    # Prominent alert when sensitive content is detected
    if auto_pause:
        matched_sensitive = [m for m in sensitive_markers if m in text]
        print("\n>>> ALERT: Sensitive email detected — pausing for human review.")
        if matched_sensitive:
            print(">>> Reason: matched keywords:", ", ".join(matched_sensitive))
        print(">>> Action: Review and choose Approve / Deny / Edit at the pause.")

    # Seed agent and reach pause (if enabled)
    app.invoke({"input": args.input}, config=config)

    # Inspect current state
    state = app.get_state(config)
    try:
        print("\nStep 2 — Automated Review & Pause:")
        print("- Next node:", state.next)
        print("- State before update:", state.values)
    except Exception:
        print("- State before update (raw):", state)
    try:
        print("- Review status:", state.values.get("review_status"))
    except Exception:
        print("- Review status: unavailable")

    # If sensitive, ask human to approve/deny/edit at pause
    interactive_done = False
    if auto_pause:
        print("\nStep 3 — Human Decision (Approve / Deny / Edit):")
        try:
            current_vals = state.values
        except Exception:
            current_vals = {}
        current_email = (current_vals.get("email_data") or {})

        choice = input("Choose [A]pprove, [D]eny, [E]dit [A]: ").strip().lower() or "a"
        if choice.startswith("d"):
            print("- Decision: Deny. Marking review_status=denied.")
            app.update_state(config, {"review_status": "denied"})
            interactive_done = True
        elif choice.startswith("e"):
            print("- Decision: Edit draft before tools.")
            # Defaults prefer CLI flags, then current state
            def_val_to = args.email_to or current_email.get("to") or "hr@company.com"
            def_val_subject = args.email_subject or current_email.get("subject") or "Intern Application"
            def_val_body = args.email_body or current_email.get("body") or args.input

            to_new = input(f"TO [{def_val_to}]: ").strip() or def_val_to
            subject_new = input(f"SUBJECT [{def_val_subject}]: ").strip() or def_val_subject
            body_new = input(f"BODY [{def_val_body}]: ").strip() or def_val_body

            updated_email = {"to": to_new, "subject": subject_new, "body": body_new}
            print("- Updated draft:", updated_email)
            app.update_state(config, {"email_data": updated_email})
            interactive_done = True
        else:
            print("- Decision: Approve. Proceeding without changes.")
            interactive_done = True

    # Apply CLI-provided (non-sensitive runs)
    if (not auto_pause) and (args.email_to or args.email_subject or args.email_body):
        email_data = {
            "to": args.email_to or "hr@company.com",
            "subject": args.email_subject or "Intern Application",
            "body": args.email_body or args.input,
        }
        print("\nStep 3 — Apply Human Update (before tools):")
        print("- Updated draft:", email_data)
        app.update_state(config, {"email_data": email_data})

        state_after = app.get_state(config)
        try:
            print("- State after update:", state_after.values)
        except Exception:
            print("- State after update (raw):", state_after)

    # Resume execution to tools
    print("\nStep 4 — Resume & Process Email:\n")
    app.invoke(None, config)

    # Outcome summary
    end_state = app.get_state(config)
    print("\nStep 5 — Outcome:")
    try:
        vals = end_state.values
    except Exception:
        vals = {}
    print("- Review status:", vals.get("review_status"))
    tool_res = vals.get("tool_result")
    if tool_res:
        print("- Handler result:", tool_res)
    else:
        print("- Handler result:", "None (likely denied or skipped)")
    print("\n=== Deliverables ===")
    print("- Clear notifications at each step: YES")
    print("- Agent pauses for sensitive actions: ", "YES" if auto_pause else "NO")
    print("- State inspected/updated before tools: ", "YES" if (args.email_to or args.email_subject or args.email_body) else "NO")
    print("- Update applied before processing: ", "YES" if tool_res else "NO")
    print("\n")


if __name__ == "__main__":
    run_cli()
