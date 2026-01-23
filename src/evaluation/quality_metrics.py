def helpfulness(reply):
    return 1 if len(reply.split()) > 3 else 0


def tone(reply):
    return 1 if "thank" in reply.lower() or "please" in reply.lower() else 0


def accuracy(pred, true):
    return 1 if pred == true else 0


def agent_quality_score(h, a, t):
    return (h + a + t) / 3
