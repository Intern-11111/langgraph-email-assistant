import requests

BASE_URL = "http://localhost:8000"


# ---------------------------
# TRIAGE EMAIL
# ---------------------------
def triage_email(email_text: str):
    payload = {
        "email": email_text,
        "from_email": "demo.sender@example.com",
        "subject": "Demo Email",
    }

    r = requests.post(f"{BASE_URL}/triage/email", json=payload)
    r.raise_for_status()
    return r.json()


# ---------------------------
# LIST PAUSED HITL THREADS
# ---------------------------
def list_hitl_threads():
    r = requests.get(f"{BASE_URL}/debug/hitl/threads")
    r.raise_for_status()
    return r.json()


# ---------------------------
# GET LOGS FOR A THREAD
# ---------------------------
def get_thread_logs(thread_id: str):
    r = requests.get(f"{BASE_URL}/debug/logs/{thread_id}")
    r.raise_for_status()
    return r.json()


# ---------------------------
# HITL DECISION
# ---------------------------
def submit_hitl_decision(
    thread_id: str,
    decision: str,
    edited_reply: str | None = None,
    to: str | None = None,
    subject: str | None = None,
):
    params = {
        "thread_id": thread_id,
        "decision": decision,
    }

    if edited_reply:
        params["edited_reply"] = edited_reply
    if to:
        params["to"] = to
    if subject:
        params["subject"] = subject

    r = requests.post(
        f"{BASE_URL}/triage/hitl/decision",
        params=params,   # 👈 QUERY PARAMS (IMPORTANT)
    )
    r.raise_for_status()
    return r.json()
