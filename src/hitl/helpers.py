# src/hitl/helpers.py
from typing import Optional

from src.graph.graph_registry import get_graph
from src.memory.store import save_memory


def resume_with_decision(
    thread_id: str,
    decision: str,
    edited_reply: Optional[str] = None,
    to: Optional[str] = None,
    subject: Optional[str] = None,
) -> None:

    graph = get_graph()

    config = {"configurable": {"thread_id": thread_id}}

    # 1) Load paused snapshot
    snapshot = graph.get_state(config=config)
    if snapshot is None:
        raise ValueError(f"No paused state found for thread_id={thread_id}")

    values = getattr(snapshot, "values", None) or getattr(snapshot, "data", None)
    if not isinstance(values, dict):
        raise TypeError(f"Unexpected snapshot container type: {type(values)}")

    # 2) Validate inputs
    if decision not in {"approve", "deny", "edit"}:
        raise ValueError("decision must be one of: approve, deny, edit")

    if decision == "edit" and not edited_reply:
        raise ValueError("edited_reply must be provided when decision='edit'")

    # 2.5) Apply human overrides (EDIT mode)
    if to:
        values["tool_payload"]["to"] = to

    if subject:
        values["tool_payload"]["subject"] = subject



    # 3) Learning step (Milestone 4)
    if decision == "edit" and edited_reply:
        email_text = (values.get("email_content") or "").lower()
        edited_text = edited_reply.lower()
        if "bob" in email_text and "robert" in edited_text:
            save_memory(namespace="preferences", key="bob", value="Robert")
            print("LEARNING: Saved preference bob → Robert")

    # 4) Inject decision into checkpointed state
    values["human_decision"] = decision
    values["edited_reply"] = edited_reply if decision == "edit" else None
    values["hitl_required"] = False  # prevent re-pausing

    print("\nHITL DECISION RECEIVED")
    print("   THREAD_ID :", thread_id)
    print("   DECISION  :", decision)
    if decision == "edit":
        print("   EDITED    :", edited_reply)

    # CRITICAL PART:
    # Update state in checkpoint, then continue execution from the pause point
    graph.update_state(config=config, values=values)

    # Continue from paused node (do NOT re-run from start)
    # Using None input tells LangGraph to resume execution with saved state.
    graph.invoke(None, config=config)

    print("GRAPH RESUMED AFTER HUMAN DECISION")
