def extract_ui_state(active_thread: dict, logs: list):
    return {
        "thread_id": active_thread.get("thread_id"),
        "draft": active_thread.get("draft_reply"),
        "selected_tool": active_thread.get("selected_tool"),
        "hitl_required": True,
        "from": active_thread.get("from"),
        "subject": active_thread.get("subject"),
        "logs": logs,
        "memory_used": {},  # optional placeholder
    }
