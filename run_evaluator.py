import json
from uuid import uuid4
from langsmith import Client
from langsmith.schemas import Example

from graph import email_agent_graph
from src.evaluation.judge_evaluator import EmailJudgeEvaluator

client = Client()

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)

examples = []

for row in load_jsonl("src/data/golden_set_emails.jsonl"):
    examples.append(
        Example(
            id=uuid4(),
            inputs={
                "subject": row["subject"],
                "body": row["body"],
            },
            outputs={
                "ideal_response": row.get("ideal_response", "")
            },
        )
    )

def email_agent(inputs):
    state = {
        "email_text": {
            "subject": inputs["subject"],
            "body": inputs["body"],
            "sender": ""
        }
    }
    final_state = email_agent_graph.invoke(state)
    return {
        "response": final_state.get("final_reply", "")
    }

client.evaluate(
    email_agent,
    data=examples,
    evaluators=[EmailJudgeEvaluator()],
    upload_results=False
)
