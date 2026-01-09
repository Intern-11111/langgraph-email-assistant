import os
import json
from typing import Any, Dict
from pathlib import Path
from dotenv import load_dotenv


from langsmith import Client
from langsmith.evaluation import evaluate, RunEvaluator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 1. SETUP ENVIRONMENT
load_dotenv()
client = Client()

JSON_FILE_PATH = "https://github.com/Intern-11111/langgraph-email-assistant/blob/ganeshsaimanideep/data/golden_emails.json"
DATASET_NAME = "Ambient_Agent_Golden_Emails"

# 2. LOAD DATASET WITH VALIDATION
def load_local_json(path_str: str):
    path = Path(path_str)
    if not path.exists():
        print(f"❌ ERROR: File not found at {path_str}")
        print("Please check if the folder names or file name are spelled correctly.")
        return None
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 3. EVALUATOR CLASS
class EmailJudgeEvaluator(RunEvaluator):
    def __init__(self):
        # Using gpt-4o for high-quality judging
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)

    def evaluate_run(self, run: Any, example: Any = None) -> Dict[str, Any]:
        agent_out = run.outputs.get("agent_summary", "No output")
        ideal_out = example.outputs.get("ideal_summary", "No reference")
        
        system_msg = "You are a strict Judge. Compare the Agent's summary to the Ideal summary. Return ONLY JSON: {\"score\": float, \"reasoning\": \"string\"}"
        user_msg = f"Ideal: {ideal_out}\nAgent: {agent_out}"
        
        try:
            res = self.llm.invoke([SystemMessage(content=system_msg), HumanMessage(content=user_msg)])
            data = json.loads(res.content.replace("```json", "").replace("```", ""))
            return {
                "key": "summary_accuracy",
                "score": data.get("score", 0.0),
                "commentary": data.get("reasoning", "N/A")
            }
        except:
            return {"key": "summary_accuracy", "score": 0.0, "commentary": "Parsing error"}

# 4. THE AGENT LOGIC (Summarization)
def ambient_agent(inputs: Dict) -> Dict:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    # This simulates the extraction/summary logic
    prompt = f"Summarize this email for a busy executive:\n\n{inputs['email_thread']}"
    response = llm.invoke(prompt)
    return {"agent_summary": response.content}

# 5. EXECUTION
if __name__ == "__main__":
    # Load the JSON
    data = load_local_json(JSON_FILE_PATH)
    
    if data:
        # Create Dataset in LangSmith if it doesn't exist
        if not client.has_dataset(dataset_name=DATASET_NAME):
            ds = client.create_dataset(DATASET_NAME)
            for item in data:
                client.create_example(
                    inputs={"email_thread": item["email_thread"]},
                    outputs={"ideal_summary": item["response_summary"]},
                    dataset_id=ds.id
                )
            print(f"Created LangSmith dataset: {DATASET_NAME}")

        print("\nRunning Evaluation on your JSON file...")
        
        
        results = evaluate(
            ambient_agent,
            data=DATASET_NAME,
            evaluators=[EmailJudgeEvaluator()],
            experiment_prefix="golden-email-test"
        )

        # 6. PRINT RESULTS HERE IN TERMINAL
        print("\n" + "="*90)
        print(f"{'EMAIL ID':<20} | {'SCORE':<5} | {'JUDGE REASONING'}")
        print("-" * 90)

        for result in results:
            # Match the ID from your JSON if possible, else use Run ID
            feedback = next((f for f in result["feedback"] if f.key == "summary_accuracy"), None)
            score = feedback.score if feedback else 0.0
            reason = feedback.commentary if feedback else "N/A"
            
            print(f"{str(result['run_id'])[:8]:<20} | {score:<5} | {reason}")
        
        print("="*90)
        print(f"\nView Traces: {results.url}\n")