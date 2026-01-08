from typing import Optional
from src.graph.graph_registry import get_graph


def resume_with_decision(
    thread_id: str,
    decision: str,
    edited_reply: Optional[str] = None,
) -> None:
    """
    Resume a paused LangGraph execution by re-invoking
    the graph with a state update and the same thread_id.
    """

    graph = get_graph()

    update = {
        "human_decision": decision
    }

    if decision == "edit" and edited_reply:
        update["edited_reply"] = edited_reply

    # 🔑 THIS is the correct "resume"
    graph.invoke(
        update,
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )
