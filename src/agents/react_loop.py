from langsmith import traceable
from src.config.tools import is_dangerous_tool
from src.graph.state import EmailState
from src.api.llm_provider import get_llm
from src.config.smith import get_project_name
import json

SYSTEM_PROMPT = """
You are a corporate email assistant.
Only reply if the triage decision is "respond".

Respond STRICTLY in this JSON format and nothing else:

{
  "thoughts": "<short reasoning>",
  "draft_reply": "<polite and concise reply>"
}
"""


@traceable(name="react_node", project_name=get_project_name())
def react_node(state: EmailState) -> EmailState:
    """
    ReAct node that:
    - Only executes if triage_decision == 'respond'
    - Uses LLM from provider to generate draft reply JSON
    """
    if state.human_decision is not None:
        return state
    
    if state.triage_decision != "respond":
        return state  # Skip — no reply needed

    llm = get_llm()

    prompt = (
        SYSTEM_PROMPT
        + "\n\nEmail content:\n"
        + state.email_content.strip()
    )

    # Invoke via LLM provider wrapper
    result = llm.invoke(prompt)

    raw_text = getattr(result, "content", str(result))

    try:
        parsed = json.loads(raw_text)
        state.agent_thoughts = parsed.get("thoughts", "")
        state.draft_reply = parsed.get("draft_reply", "")
    except Exception:
        # Fallback if model returns malformed JSON
        state.agent_thoughts = "Model returned text not valid JSON."
        state.draft_reply = raw_text

    print("LLM GENERATED DRAFT")
    print("THOUGHTS:", state.agent_thoughts)
    print("DRAFT REPLY:")
    print(state.draft_reply)

        # Planned irreversible action
    state.selected_tool = "send_email"
    state.tool_payload = {
        "body": state.draft_reply
    }

    #  Tag dangerous tool → triggers HITL later in graph
    if is_dangerous_tool(state.selected_tool):
        state.hitl_required = True

    return state
