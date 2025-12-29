def run_email_agent(email_text: str) -> str:
    text = email_text.lower().strip()

    if len(text) < 20:
        return "ignore"

    risky_phrases = ["urgent", "as discussed", "do the needful", "immediately"]
    if any(phrase in text for phrase in risky_phrases):
        return "notify_human"

    return "respond"
