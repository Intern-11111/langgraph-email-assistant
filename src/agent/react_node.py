import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class ReasonNode:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
You are an email assistant.

Email:
Subject: {subject}
Body: {body}

Decide the next action.

Available actions:
- read_calendar
- lookup_contact
- reply

Respond ONLY in valid JSON like:
{{
  "thought": "...",
  "action": "...",
  "action_input": {{ }}
}}
Use ONLY these actions:
reply, send_email, delete_email, create_calendar_event
"""
        )

    def __call__(self, state: dict) -> dict:
        triage = state.get("triage_result", {})
        label = triage.get("final_label", "").strip().lower()

        # 🚫 Stop if not reason_act
        if label != "reason_act":
            state["reasoning"] = [{
                "thought": f"Triage blocked reasoning (label={label})",
                "action": None,
                "action_input": None
            }]
            return state

        response = self.llm.invoke(
            self.prompt.format(
                subject=state["email_text"]["subject"],
                body=state["email_text"]["body"]
            )
        )

        try:
            decision = json.loads(response.content)
        except Exception as e:
            state["reasoning"] = [{
                "thought": f"JSON parse error: {str(e)}",
                "action": None,
                "action_input": None
            }]
            return state

        state["reasoning"] = [{
            "thought": decision.get("thought"),
            "action": decision.get("action"),
            "action_input": decision.get("action_input", {})
        }]

        return state
