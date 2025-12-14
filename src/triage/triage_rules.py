class RuleBasedTriage:
    """
    Rule-based triage
    Categories returned:
      - ignore
      - notify_human
      - reason_act
    """

    def classify(self, subject: str, body: str, sender: str = "") -> dict:
        """
        Returns:
            {
                "label": "ignore/notify_human/reason_act",
                "confidence": float
            }
        """

        text = f"{subject} {body}".lower()

        # -------- IGNORE CATEGORY --------
        if any(w in text for w in ["unsubscribe", "spam", "lottery", "promotion", "newsletter"]):
            return {"label": "ignore", "confidence": 0.95}

        # -------- NOTIFY HUMAN CATEGORY --------
        if any(w in text for w in ["urgent", "complaint", "angry", "issue", "problem", "fail", "refund"]):
            return {"label": "notify_human", "confidence": 0.90}

        # -------- REASON/ACT CATEGORY --------
        if any(w in text for w in ["meeting", "schedule", "call", "zoom", "availability", "contact", "email", "question"]):
            return {"label": "reason_act", "confidence": 0.85}

        # Default fallback
        return {"label": "reason_act", "confidence": 0.60}
