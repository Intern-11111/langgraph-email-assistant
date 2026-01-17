import json
import os
import time
from typing import List, Dict

from src.graph.state import EmailState

# Load the LangGraph agent
from src.graph.graph_registry import get_graph

graph = get_graph()


# Scoring weights for rubric
WEIGHTS = {
    "triage": 0.50,
    "reply": 0.20,
    "tone": 0.10,
    "format": 0.10,
    "latency": 0.05,
    "hallucination": 0.05,
}

POLITE_WORDS = ["thanks", "thank you", "please", "appreciate", "glad"]


def score_triage(predicted: str, ideal: str) -> float:
    return 1.0 if predicted == ideal else 0.0


def score_reply(reply: str, ideal_reply: str) -> float:
    if not ideal_reply.strip():
        return 0.0

    ideal_tokens = ideal_reply.lower().split()
    reply_tokens = reply.lower().split()

    overlap = len(set(ideal_tokens) & set(reply_tokens))
    return min(overlap / len(ideal_tokens), 1.0)


def score_tone(reply: str) -> float:
    return 1.0 if any(word in reply.lower() for word in POLITE_WORDS) else 0.0


def score_format(predicted: str) -> float:
    return 1.0 if predicted in ["ignore", "respond", "notify_human"] else 0.0


def score_hallucination(reply: str, email: str) -> float:
    # If reply contains content not hinted in email → reduce score
    return 1.0 if reply.strip() == "" or reply.lower() in email.lower() else 0.5


def score_latency(seconds: float) -> float:
    if seconds <= 2: return 1.0
    if seconds <= 6: return 0.5
    return 0.0


def extract_output_fields(output):
    """Make output work for dict or EmailState object"""
    if isinstance(output, dict):
        predicted = output.get("triage_decision")
        reply = output.get("draft_reply", "")
        reason = output.get("triage_reason", "")
    else:
        predicted = output.triage_decision
        reply = getattr(output, "draft_reply", "")
        reason = getattr(output, "triage_reason", "")
    return predicted, reply, reason


def evaluate_dataset(dataset: List[Dict]):
    results = []
    correct = 0

    for item in dataset:
        state = EmailState(email_content=item["email"])

        start_time = time.time()
        thread_id = f"eval-{hash(item['email'])}"

        output = graph.invoke(
            state,
            config={"configurable": {"thread_id": thread_id}}
        )

        latency = time.time() - start_time

        predicted, reply, reason = extract_output_fields(output)
        ideal = item["ideal_label"]

        # Subscores
        s_triage = score_triage(predicted, ideal)
        s_reply = score_reply(reply, item.get("ideal_reply", ""))
        s_tone = score_tone(reply)
        s_format = score_format(predicted)
        s_latency = score_latency(latency)
        s_hallucination = score_hallucination(reply, item["email"])

        # Weighted final score
        final_score = round(
            s_triage * WEIGHTS["triage"] +
            s_reply * WEIGHTS["reply"] +
            s_tone * WEIGHTS["tone"] +
            s_format * WEIGHTS["format"] +
            s_latency * WEIGHTS["latency"] +
            s_hallucination * WEIGHTS["hallucination"],
            2,
        )

        if predicted == ideal:
            correct += 1

        results.append({
            "email": item["email"][:120] + "...",
            "ideal": ideal,
            "predicted": predicted,
            "triage_score": s_triage,
            "reply_score": s_reply,
            "tone_score": s_tone,
            "format_score": s_format,
            "latency_sec": round(latency, 2),
            "latency_score": s_latency,
            "hallucination_score": s_hallucination,
            "agent_quality_score": final_score,
            "reason": reason,
        })

    accuracy = correct / len(dataset)

    return {
        "total": len(dataset),
        "correct_predictions": correct,
        "accuracy": round(accuracy, 3),
        "avg_quality_score": round(sum(r["agent_quality_score"] for r in results) / len(results), 2),
        "results": results,
    }


def run_full_evaluation():
    base_path = "data"
    files = [
        "m2_testset_batch1_respond.json",
        "m2_testset_batch2_notify.json",
        "m2_testset_batch3_ignore.json"
    ]

    combined = []
    for f in files:
        with open(os.path.join(base_path, f), "r", encoding="utf-8") as fp:
            combined.extend(json.load(fp))

    return evaluate_dataset(combined)
