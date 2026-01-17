from langsmith import traceable
from src.config.tools import is_dangerous_tool
from src.graph.state import EmailState
from src.api.llm_provider import get_llm
from src.config.smith import get_project_name
from src.memory.store import load_memory
from src.utils.time import now_local, USER_TZ
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from src.utils.logger import log
from src.utils.enforce import enforce_name_preference


import json
import re

SYSTEM_PROMPT = """
You are a professional corporate email assistant.

TASK:
Read the given email content and draft a polite, concise, and professional reply.

OUTPUT FORMAT (STRICTLY ENFORCED):
- Output MUST be a single, valid JSON object.
- Output MUST NOT include markdown.
- Output MUST NOT include explanations, notes, or commentary.
- Output MUST NOT include code blocks.
- Output MUST NOT include any text before or after the JSON.

REQUIRED JSON KEYS:
- "thoughts": a brief internal reasoning summary (1 sentence).
- "draft_reply": the final email reply written in a professional tone.

IMPORTANT:
- If information is missing, make a reasonable professional assumption.
- If the request is unclear, draft a neutral acknowledgment reply.
- Even if unsure, ALWAYS return valid JSON.

FINAL INSTRUCTION:
Return ONLY the JSON object and nothing else.
"""


def safe_parse_llm_json(raw_text: str) -> dict:
    try:
        parsed = json.loads(raw_text)
        if isinstance(parsed, dict) and "draft_reply" in parsed:
            return {
                "thoughts": parsed.get("thoughts", "No explicit reasoning provided."),
                "draft_reply": str(parsed["draft_reply"]).strip(),
            }
    except Exception:
        pass

    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group())
            if isinstance(parsed, dict) and "draft_reply" in parsed:
                return {
                    "thoughts": parsed.get("thoughts", "Recovered from partial JSON."),
                    "draft_reply": str(parsed["draft_reply"]).strip(),
                }
        except Exception:
            pass

    clean_text = (raw_text or "").strip()
    if clean_text.startswith("{") or not clean_text:
        clean_text = "Thank you for your email. I will get back to you shortly."

    return {
        "thoughts": "Fallback due to invalid or truncated JSON from LLM.",
        "draft_reply": clean_text,
    }


@traceable(name="react_node", project_name=get_project_name())
def react_node(state: EmailState) -> EmailState:

    # Resume safety
    if state.human_decision is not None:
        print("React node skipped (resuming after HITL)")
        return state

    # TEMP: do NOT block on triage until stable
    # if state.triage_decision != "respond":
    #     return state

    # LOAD MEMORY
    preferences = load_memory("preferences")
    name_pref = preferences.get("name")

    memory_context = ""
    if name_pref:
        memory_context = (
            f"\nSYSTEM RULE (MANDATORY):\n"
            f"- The sender MUST be addressed as '{name_pref}'.\n"
            f"- ALWAYS use this name in the greeting.\n"
            f"- Ignore the email signature if it uses a different name.\n"
        )


    # LLM
    llm = get_llm()
    prompt = (
        SYSTEM_PROMPT
        + memory_context
        + "\nEmail content:\n"
        + (state.email_content or "").strip()
        + "\n\nJSON SCHEMA:\n"
        "{ \"thoughts\": string, \"draft_reply\": string }"
    )

    result = llm.invoke(prompt)
    raw_text = getattr(result, "content", str(result))
    parsed = safe_parse_llm_json(raw_text)

    state.agent_thoughts = parsed["thoughts"]

    draft = parsed["draft_reply"]

    # HARD MEMORY ENFORCEMENT (SYSTEM LEVEL)
    if name_pref:
        draft = enforce_name_preference(draft, name_pref)

    state.draft_reply = draft


    log(state, "LLM GENERATED DRAFT")
    log(state, f"DRAFT: {state.draft_reply}")


    # TOOL SELECTION
    text = (state.email_content or "").lower()

    if any(k in text for k in ["meeting", "schedule", "calendar"]):
        base_time = now_local()
        meeting_date = (base_time + timedelta(days=1)).date()

        start_dt = datetime(
            meeting_date.year,
            meeting_date.month,
            meeting_date.day,
            15, 0, tzinfo=USER_TZ
        )

        end_dt = start_dt + timedelta(minutes=30)

        state.selected_tool = "read_calendar"
        state.tool_payload = {
            "title": "Meeting",
            "start_time": start_dt.isoformat(),
            "end_time": end_dt.isoformat(),
            "to": state.from_email,
            "subject": f"Re: {state.subject}",
            "body": state.draft_reply,
        }

    else:
        state.selected_tool = "send_email"
        state.tool_payload = {
            "to": state.from_email,
            "subject": f"Re: {state.subject}",
            "body": state.draft_reply,
        }

    # Let SAFE TOOL decide HITL
    state.hitl_required = False

    log(state, f"PLANNED TOOL: {state.selected_tool}")

    return state


