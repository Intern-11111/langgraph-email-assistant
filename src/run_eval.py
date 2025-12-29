import time
from langsmith import evaluate, Client
from triage_agent import triage_email
from dotenv import load_dotenv

load_dotenv()
client = Client()

DATASET_NAME = "Email_Assistant_Triage_Golden_Set"

def target_function(inputs: dict) -> dict:
    # Add a 4-second delay to stay under 15 requests per minute
    time.sleep(4) 
    email_text = inputs.get("email_body", "")
    prediction = triage_email(email_text)
    return {"triage_prediction": prediction}

def check_accuracy(run, example):
    reference = example.outputs.get("triage")
    prediction = run.outputs.get("triage_prediction")
    score = 1 if prediction == reference else 0
    return {"key": "triage_accuracy", "score": score}

if __name__ == "__main__":
    results = evaluate(
        target_function,
        data=DATASET_NAME,
        evaluators=[check_accuracy],
        experiment_prefix="Milestone-2-Final-Success",
        max_concurrency=1  # Keep this at 1 to prevent rate limit errors
    )