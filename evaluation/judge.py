# Compare agent_reply vs ideal_reply
# Score on Helpfulness, Tone, Accuracy
# Return JSON

from evaluation.metrics import (
    score_helpfulness,
    score_tone,
    score_accuracy
)

def evaluate(agent_reply, ideal_reply):
    return {
        "helpfulness": score_helpfulness(agent_reply, ideal_reply),
        "tone": score_tone(agent_reply),
        "accuracy": score_accuracy(agent_reply, ideal_reply),
    }
