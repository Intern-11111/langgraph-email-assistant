from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from triage.triage_node import TriageNode


def triage_node(state: dict) -> dict:

    #Returns a dict: {"label": str, "confidence": float, "source": "rules" | "llm"}.
    
    triage = TriageNode()

    # Allow simple input via `email_text`
    email_text = state.get("email_text", "")
    subject = state.get("subject", "")
    body = state.get("body", "")
    sender = state.get("sender", "")

    if email_text and not (subject or body):
        # Treat the text as body; subject left empty
        body = email_text

    result = triage.run({
        "subject": subject,
        "body": body,
        "sender": sender,
    })

    return {
        "label": result.get("final_label"),
        "confidence": result.get("final_confidence"),
        "source": result.get("source"),
    }


def create_triage_workflow():
    """
    Builds the LangGraph workflow for the triage system.
    The graph has ONE node: triage_node
    Input: {"email_text": "..."}
    Output: {"label": "...", "confidence": float, "source": "rule" | "llm"}
    """

    workflow = StateGraph(dict)

    # Add node
    workflow.add_node("triage", triage_node)

    # Set entry & finish
    workflow.set_entry_point("triage")
    workflow.set_finish_point("triage")

    # Compile without checkpointer for simple run
    return workflow.compile()


if __name__ == "__main__":
    graph = create_triage_workflow()

    # Example run
    result = graph.invoke({"email_text": "Congratulations, you won a free iPhone!"})
    print(result)
