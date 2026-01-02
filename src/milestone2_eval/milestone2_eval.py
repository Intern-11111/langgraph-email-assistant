from langsmith import Client
from langsmith.schemas import Example
from uuid import uuid4
import csv
from agents.test_email_agent import email_agent_chain
from evaluation.eval.test_email_eval import EmailJudgeEvaluator

client = Client()

dataset_uuid = uuid4()
examples: list[Example] = []
with open("data/test_emails.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        examples.append(
            Example(
                id=uuid4(),
                dataset_id=dataset_uuid,
                inputs={
                    "subject": row.get("subject", ""),
                    "body": row.get("body", ""),
                },
                outputs={"ideal_response": row.get("ideal_response", "")},
            )
        )

# Use the modern evaluation API with local examples and no upload
client.evaluate(
    email_agent_chain(),
    data=examples,
    evaluators=[EmailJudgeEvaluator()],
    max_concurrency=1,
    upload_results=False,
)
