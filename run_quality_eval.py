# Agent Quality Score =(Helpfulness + Accuracy + Tone) / 3

from src.evaluation.scoring import compute_agent_quality_score

judge_scores = {
    "helpfulness": 4,
    "accuracy": 5,
    "tone": 4
}

final_score = compute_agent_quality_score(judge_scores)

print("Judge Scores:", judge_scores)
print("Final Agent Quality Score:", round(final_score, 2))
