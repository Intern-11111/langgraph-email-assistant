import json
from typing import Any, Dict

from langsmith.evaluation import RunEvaluator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class EmailJudgeEvaluator(RunEvaluator):
    """
    LLM-based evaluator for email agent responses.
    Compares agent output vs reference (ideal) output.
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=300,
        )

    def evaluate_run(
        self,
        run,
        example=None,
        **kwargs,  
    ) -> Dict[str, Any]:

        try:
            # Extract inputs & outputs
            email_body = run.inputs.get("email_body", "")
            agent_response = run.outputs.get("response", "")

            ideal_response = ""
            if example and example.outputs:
                ideal_response = example.outputs.get("ideal_response", "")

            # Build judge prompt
            system_prompt = """
You are a strict evaluation judge.

You MUST return ONLY valid JSON.
DO NOT include explanations, markdown, or text outside JSON.

Schema:
{
  "accuracy": number (0-1),
  "helpfulness": number (0-1),
  "tone": number (0-1),
  "overall": number (0-1)
}
"""

            user_prompt = f"""
Email:
{email_body}

Agent Response:
{agent_response}

Ideal Response:
{ideal_response}

Evaluate the agent response against the ideal response.
Return JSON only.
"""

            messages = [
                SystemMessage(content=system_prompt.strip()),
                HumanMessage(content=user_prompt.strip()),
            ]

            result = self.llm.invoke(messages)
            raw_output = result.content.strip()

            # Safe JSON parsing
            scores = self._safe_parse_json(raw_output)

            # Return LangSmith-compatible format
            return {
                "key": "email_quality",
                "score": scores.get("overall", 0.0),
                "metrics": {
                    "accuracy": scores.get("accuracy", 0.0),
                    "helpfulness": scores.get("helpfulness", 0.0),
                    "tone": scores.get("tone", 0.0),
                },
                "commentary": raw_output,
            }

        except Exception as e:

            return {
                "key": "email_quality",
                "score": 0.0,
                "metrics": {
                    "accuracy": 0.0,
                    "helpfulness": 0.0,
                    "tone": 0.0,
                },
                "commentary": f"Evaluator error: {str(e)}",
            }

    def _safe_parse_json(self, text: str) -> Dict[str, float]:

        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start == -1 or end == -1:
                raise ValueError("No JSON found")

            data = json.loads(text[start:end])

            return {
                "accuracy": float(data.get("accuracy", 0)),
                "helpfulness": float(data.get("helpfulness", 0)),
                "tone": float(data.get("tone", 0)),
                "overall": float(data.get("overall", 0)),
            }

        except Exception:
            return {
                "accuracy": 0.0,
                "helpfulness": 0.0,
                "tone": 0.0,
                "overall": 0.0,
            }
