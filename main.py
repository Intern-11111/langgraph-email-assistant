# main.py

from dotenv import load_dotenv
load_dotenv()

import os
import sys
from datetime import datetime

# Allow src imports
sys.path.append(os.path.abspath("src"))

from hitl_graph import build_hitl_graph
from mock_tools import (
    mock_send_email,
    mock_ignore_email,
    mock_sensitive_action,
    mock_deny_action
)

LOG_FILE = "test_case_log.txt"


def log_result(entry: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


def run_email(email_body: str, approved: bool | None = None):
    app = build_hitl_graph()

    print("\n📨 Incoming Email:")
    print(email_body)

    try:
        result = app.invoke(
            {"email_body": email_body},
            config={"configurable": {"thread_id": "main-run"}},
        )

        # --- NEW LOGIC INTEGRATED ---
        decision = result.get("decision")
        approved_status = approved if approved is not None else result.get("approved")

        if decision == "respond":
            print("✅ Responding to email automatically")
            mock_send_email()
            log_result(f"[{datetime.now()}] SAFE | Decision=respond | Email='{email_body}'")

        elif decision == "ignore":
            print("ℹ️ Ignoring email")
            mock_ignore_email()
            log_result(f"[{datetime.now()}] SAFE | Decision=ignore | Email='{email_body}'")

        elif decision == "notify_human":
            print("⏸️ Human intervention required")
            if approved_status:
                print("✅ Human approved action")
                mock_sensitive_action(email_body)
                log_result(f"[{datetime.now()}] DANGEROUS | Approved=True | Email='{email_body}'")
            else:
                print("❌ Human rejected action")
                mock_deny_action()
                log_result(f"[{datetime.now()}] DANGEROUS | Approved=False | Email='{email_body}'")

        else:
            print("⚠️ Unknown decision received:", decision)
            log_result(f"[{datetime.now()}] UNKNOWN | Decision={decision} | Email='{email_body}'")

    except Exception as e:
        print("❌ Error during execution:", e)
        log_result(f"[{datetime.now()}] ERROR | Exception={e} | Email='{email_body}'")


if __name__ == "__main__":
    # --- SAFE EMAIL ---
    run_email("Please schedule a meeting for tomorrow")

    # --- DANGEROUS (REJECTED) ---
    run_email("Delete all production data immediately", approved=False)

    # --- DANGEROUS (APPROVED) ---
    run_email("Reset all admin passwords immediately", approved=True)
