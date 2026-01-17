import base64
import json
from fastapi import APIRouter

from src.state.thread_registry import THREAD_REGISTRY
from src.graph.graph_registry import get_graph
from src.graph.state import EmailState
from src.integrations.gmail import fetch_latest_email

router = APIRouter(prefix="/gmail", tags=["Gmail"])

PROCESSED = set()

@router.post("/webhook")
def gmail_webhook(payload: dict):
    # --------------------------------------------------
    # Decode Pub/Sub message
    # --------------------------------------------------
    try:
        message = payload.get("message", {})
        data = message.get("data")

        if not data:
            return {"status": "ignored", "reason": "no data"}

        decoded = base64.b64decode(data).decode()
        event = json.loads(decoded)

    except Exception as e:
        print("Webhook decode error:", e)
        return {"status": "error", "error": str(e)}

    # --------------------------------------------------
    # Fetch latest Gmail message
    # --------------------------------------------------
    email = fetch_latest_email()
    if not email:
        return {"status": "ignored", "reason": "no email found"}

    msg_id = email["message_id"]

    # --------------------------------------------------
    # De-duplication
    # --------------------------------------------------
    if msg_id in PROCESSED:
        return {"status": "ignored", "reason": "duplicate"}

    PROCESSED.add(msg_id)

    # --------------------------------------------------
    # REGISTER THREAD (🔥 THIS WAS MISSING)
    # --------------------------------------------------
    THREAD_REGISTRY.add(msg_id)

    # --------------------------------------------------
    # Invoke LangGraph
    # --------------------------------------------------
    graph = get_graph()

    state = EmailState(
        email_content=email["body"],
        from_email=email["from"],
        subject=email["subject"],
    )

    try:
        graph.invoke(
            state,
            config={
                "configurable": {
                    "thread_id": msg_id
                }
            }
        )
    except Exception as e:
        print("Graph execution error:", e)

    print("⏸ HITL THREAD_ID:", msg_id)

    # --------------------------------------------------
    # Always ACK Pub/Sub
    # --------------------------------------------------
    return {"status": "ok"}
