import json
from langchain.chat_models.base import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

class LLMFallbackTriage:
    """
    LLM fallback triage.
    """
    def __init__(self):
        load_dotenv()
        self.model = init_chat_model(
            model="gpt-4o-mini",  
            temperature=0.2,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.allowed_labels = ["ignore", "notify_human", "reason_act"]

    def classify(self, subject: str, body: str) -> dict:
        prompt = ChatPromptTemplate.from_template("""
Classify the email into one of these categories:

1. ignore
2. notify_human
3. reason_act

Return JSON ONLY:
{{
  "label": "ignore | notify_human | reason_act",
  "confidence": 0.xx
}}

Subject: {subject}
Body: {body}
""")

        chain = prompt | self.model
        response = chain.invoke({"subject": subject, "body": body})

        try:
            data = json.loads(response.content)
        except Exception:
            data = {"label": "reason_act", "confidence": 0.5}

        if data["label"] not in self.allowed_labels:
            data["label"] = "reason_act"

        data["confidence"] = min(max(data.get("confidence", 0.5), 0), 1)
        data["source"] = "llm"

        return data
