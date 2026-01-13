# | Metric      | Meaning                  |
# | ----------- | ------------------------ |
# | Helpfulness | Answer addresses request |
# | Tone        | Polite & professional    |
# | Accuracy    | Matches intent           |

def score_helpfulness(agent_reply, ideal_reply):
    return 5 if agent_reply and ideal_reply else 1

def score_tone(agent_reply):
    polite_words = ["thank", "please", "appreciate"]
    return 5 if any(w in agent_reply.lower() for w in polite_words) else 3

def score_accuracy(agent_reply, ideal_reply):
    return 5 if agent_reply == ideal_reply else 3
