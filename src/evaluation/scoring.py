def compute_agent_quality_score(scores: dict):
    """
    scores = {
        "helpfulness": 4,
        "accuracy": 5,
        "tone": 4
    }
    """
    return sum(scores.values()) / len(scores)
