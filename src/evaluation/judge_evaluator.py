import json
import os
from dotenv import load_dotenv
from typing import Any, Dict
from langsmith.evaluation import RunEvaluator
from langchain.chat_models.base import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage


class EmailJudgeEvaluator(RunEvaluator):

    def __init__(self):
       load_dotenv()
       self.llm = init_chat_model(
        model="gpt-4o-mini",
        temperature=0.2,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )


    def evaluate_run(self, run, example=None, **kwargs) -> Dict[str, Any]:

        email_subject = run.inputs.get("subject", "")
        email_body = run.inputs.get("body", "")
        agent_response = run.outputs.get("response", "")

        ideal_response = ""
        if example and example.outputs:
            ideal_response = example.outputs.get("ideal_response", "")

        system_prompt = """
You are an evaluation judge.

Score the agent response from 1 to 5 on:
- accuracy
- helpfulness
- tone
- safety
- conciseness

Return ONLY valid JSON.

Schema:
{
  "accuracy": number,
  "helpfulness": number,
  "tone": number,
  "safety": number,
  "conciseness": number,
  "overall": number
}

overall = average of all metrics.
"""

        user_prompt = f"""
Email Subject:
{email_subject}

Email Body:
{email_body}

Agent Response:
{agent_response}

Ideal Response:
{ideal_response}
"""

        result = self.llm.invoke([
            SystemMessage(content=system_prompt.strip()),
            HumanMessage(content=user_prompt.strip())
        ])

        scores = self._safe_parse_json(result.content)

        return {
            "key": "email_quality",
            "score": scores["overall"],
            "metrics": scores,
            "commentary": result.content
        }

    def _safe_parse_json(self, text: str) -> Dict[str, float]:
        try:
            data = json.loads(text[text.find("{"):text.rfind("}") + 1])
            return {
                "accuracy": float(data.get("accuracy", 0)),
                "helpfulness": float(data.get("helpfulness", 0)),
                "tone": float(data.get("tone", 0)),
                "safety": float(data.get("safety", 0)),
                "conciseness": float(data.get("conciseness", 0)),
                "overall": float(data.get("overall", 0)),
            }
        except Exception:
            return {
                "accuracy": 0,
                "helpfulness": 0,
                "tone": 0,
                "safety": 0,
                "conciseness": 0,
                "overall": 0,
            }
