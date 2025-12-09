from langsmith import traceable
from src.graph.state import EmailState
from src.api.llm_provider import get_llm
from src.config.smith import get_project_name


SYSTEM_PROMPT = """You are an email assistant.

You receive an email and a triage decision of 'respond'.
Your job is to:
1) Think briefly about what the user wants.
2) Draft a short, polite reply email.

Reply STRICTLY in the following JSON format:

{
  "thoughts": "<1-2 sentence explanation of what you will do>",
  "draft_reply": "<the email reply body>"
}
"""


@traceable(name="react_loop", project_name=get_project_name())
def react_node(state: EmailState) -> EmailState:
    """
    Basic ReAct-like node for Milestone 1.

    - Only runs if triage_decision == 'respond'
    - Uses the LLM to generate:
        - agent_thoughts
        - draft_reply
    - For ignore / notify_human, it leaves state untouched.
    """
    # If we don't need to respond, skip ReAct logic
    if state.triage_decision != "respond":
        return state

    llm = get_llm()

    prompt = (
        SYSTEM_PROMPT
        + "\n\nEmail:\n"
        + state.email_content.strip()
    )

    # For chat or text LLMs via LangChain, .invoke() is the unified call
    result = llm.invoke(prompt)

    # Some models return .content (chat-style), others a raw string (pipeline)
    if hasattr(result, "content"):
        raw_text = result.content
    else:
        raw_text = str(result)

    # Try to parse JSON; if it fails, just put everything in draft_reply
    import json

    try:
        parsed = json.loads(raw_text)
        state.agent_thoughts = parsed.get("thoughts")
        state.draft_reply = parsed.get("draft_reply", raw_text)
    except Exception:
        state.agent_thoughts = "LLM did not return valid JSON. Raw output stored as draft_reply."
        state.draft_reply = raw_text

    return state
