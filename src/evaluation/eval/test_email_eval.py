import json
import time
from langsmith.evaluation import RunEvaluator
from langchain_openai import ChatOpenAI
import openai
from openai import RateLimitError, APIError as OpenAIError

# Load Intern 2 metrics
with open("src/evaluation/Metrics/agent_quality_metrics.json") as f:
    METRICS = json.load(f)["metrics"]

METRIC_NAMES = [m["name"] for m in METRICS]

# Initialize Judge LLM
judge_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def call_judge_with_retry(prompt, max_retries=5, wait_base=10):
    """
    Call LLM with automatic retry on rate limits or OpenAI errors.
    Uses exponential backoff and returns LLM output.
    """
    for i in range(max_retries):
        try:
            response = judge_llm.invoke(prompt).content
            if not response.strip():
                raise ValueError("Empty response from LLM")
            return response
        except RateLimitError as e:
            wait_time = wait_base * (i + 1)
            print(f"[RateLimitError] Retry {i+1}/{max_retries} in {wait_time}s...")
            time.sleep(wait_time)
        except OpenAIError as e:
            print(f"[OpenAIError] {e}, retrying {i+1}/{max_retries}...")
            time.sleep(5)
        except ValueError as e:
            print(f"[Warning] {e}, retrying {i+1}/{max_retries}...")
            time.sleep(5)
    raise Exception("Max retries exceeded for judge LLM.")

class EmailJudgeEvaluator(RunEvaluator):
    def evaluate_run(self, run, example, **kwargs):
        """
        Evaluate a single agent run.
        **kwargs: Accepts extra arguments from LangSmith (e.g., evaluator_run_id)
        """
        agent_response = run.outputs.get("response", "")
        email_body = example.inputs.get("body", "")
        ideal_response = example.outputs.get("ideal_response", "")

        metric_list = "\n".join([f"- {name} (1–5)" for name in METRIC_NAMES])

        # Load prompt template
        with open("evaluation/judge_prompts/email_judge_prompt.txt") as f:
            prompt_template = f.read()

        prompt = prompt_template.format(
            email_body=email_body,
            agent_response=agent_response,
            ideal_response=ideal_response,
            metric_list=metric_list
        )

        # Call LLM with retry
        judge_output = call_judge_with_retry(prompt)

        # Ensure JSON parsing
        try:
            scores = json.loads(judge_output)
        except json.JSONDecodeError:
            print("[Warning] Judge returned invalid JSON, returning default 0 scores")
            scores = {name: 0 for name in METRIC_NAMES}
            scores["final_score"] = 0

        return {
            "key": "milestone2_agent_quality_score",
            "score": scores.get("final_score", 0),
            "commentary": scores
        }
