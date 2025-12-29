class RuleBasedTriage:
    """
    Dataset-agnostic rule-based triage.
    Rules detect intent, not specific email content.
    """

    def classify(self, subject: str, body: str, sender: str = "") -> dict:
        text = f"{subject} {body}".lower()

        # -------- IGNORE --------
        if any(w in text for w in [
            "unsubscribe", "promotion", "offer", "discount",
            "free", "deal", "limited time", "win", "reward",
            "click here", "act now"
        ]):
            return {"label": "ignore", "confidence": 0.90}

        # -------- REASON / ACT --------
        if any(w in text for w in [
            "verify", "confirm", "approve", "deny",
            "login", "security", "otp", "password",
            "payment", "billing", "invoice", "bank",
            "interview", "job", "offer", "resume",
            "request", "action required"
        ]):
            return {"label": "reason_act", "confidence": 0.88}

        # -------- NOTIFY HUMAN --------
        if any(w in text for w in [
            "update", "reminder", "notification",
            "alert", "maintenance", "scheduled",
            "delivered", "shipped", "completed"
        ]):
            return {"label": "notify_human", "confidence": 0.85}

        # Low-confidence fallback → let LLM decide
        return {"label": "reason_act", "confidence": 0.55}
