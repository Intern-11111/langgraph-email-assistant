# src/api/debug_router.py
from fastapi import APIRouter
from src.state.thread_registry import THREAD_REGISTRY
from src.graph.graph_registry import get_graph

router = APIRouter(prefix="/debug", tags=["Debug"])

graph = get_graph()

@router.get("/hitl/threads")
def list_hitl_threads():
    paused = []

    for thread_id in list(THREAD_REGISTRY):
        try:
            state = graph.get_state(
                config={"configurable": {"thread_id": thread_id}}
            ).values

            if state.get("hitl_required") and state.get("human_decision") is None:
                paused.append({
                    "thread_id": thread_id,
                    "selected_tool": state.get("selected_tool"),
                    "draft_reply": state.get("draft_reply"),
                    "from": state.get("from_email"),
                    "subject": state.get("subject"),
                })
        except Exception:
            continue

    return {
        "paused_threads": paused,
        "count": len(paused),
    }

@router.get("/logs/{thread_id}")
def get_thread_logs(thread_id: str):
    """
    Read-only endpoint to inspect agent execution logs
    for a given HITL thread.
    """
    try:
        state = graph.get_state(
            config={"configurable": {"thread_id": thread_id}}
        ).values
    except Exception:
        return {
            "error": "Invalid or expired thread_id"
        }

    return {
        "thread_id": thread_id,
        "execution_logs": state.get("execution_logs", []),
    }
