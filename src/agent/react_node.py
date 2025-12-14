import json
import os
from dotenv import load_dotenv
from langchain.chat_models.base import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

class ReasonNode:
    """
    Decides what action to take after triage using OpenAI.
    """

    def __init__(self):
        load_dotenv()
        self.model = init_chat_model(
            model="gpt-4o-mini",  
            temperature=0.2,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        self.prompt = ChatPromptTemplate.from_template(
"""
You are an email assistant.
Email:
Subject: {subject}
Body: {body}

Return JSON ONLY:
{
  "thought": "reasoning",
  "action": "read_calendar | lookup_contact | reply",
  "action_input": {}
}
"""
        )

    # LangGraph entry point
    def __call__(self, state: dict) -> dict:
        triage_label = state.get("triage", {}).get("label")
        email = state.get("email", {})

        if triage_label != "reason_act":
            state["reasoning"] = [{
                "thought": "Triage blocked reasoning",
                "action": None,
                "action_input": None
            }]
            return state

        subject = email.get("subject", "")
        body = email.get("body", "")

        # Combine prompt and model
        chain = self.prompt | self.model
        response = chain.invoke({"subject": subject, "body": body})

        try:
            parsed = json.loads(response.content)
        except Exception:
            parsed = {
                "thought": "Fallback",
                "action": "reply",
                "action_input": {
                    "message": "Thanks for your email!"
                }
            }

        state["reasoning"] = [parsed]
        return state
