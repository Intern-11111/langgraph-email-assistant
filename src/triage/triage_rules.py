class RuleBasedTriage:
    """
    Rule-based triage.
    Deterministic and high-confidence for common intents.
    """

    def classify(self, subject: str, body: str, sender: str = "") -> dict:
        text = f"{subject} {body}".lower()

        # -------- IGNORE --------
        if any(w in text for w in [
            "unsubscribe", "promotion", "offer", "discount",
            "free", "deal", "limited time", "win", "reward",
            "click here", "act now","Newsletter"
        ]):
            return {"label": "ignore", "confidence": 0.95}

        # -------- MEETINGS / CONTACTS (REASON_ACT) --------
        if any(w in text for w in [
            "meeting", "schedule", "calendar", "appointment",
            "call", "availability", "reschedule",
            "contact", "email address", "phone number"
        ]):
            return {"label": "reason_act", "confidence": 0.95}

        # -------- ACTION / TRANSACTION --------
        if any(w in text for w in [
            "verify", "confirm", "approve", "deny",
            "login", "security", "otp", "password",
            "payment", "billing", "invoice", "bank",
            "request", "action required"
        ]):
            return {"label": "reason_act", "confidence": 0.90}

        # -------- NOTIFY HUMAN --------
        if any(w in text for w in [
            "update", "reminder", "notification",
            "alert", "maintenance", "scheduled",
            "delivered", "shipped", "completed"
        ]):
            return {"label": "notify_human", "confidence": 0.85}

        # Fallback → LLM
        return {"label": "reason_act", "confidence": 0.40}
