def triage_email(state):
    email = state["email"].lower()

    IGNORE_KEYWORDS = [
        "unsubscribe", "offer", "sale", "discount", "promotion",
        "deal", "cashback", "buy", "free", "advertisement",
        "coupon", "newsletter", "marketing"
    ]

    RESPOND_KEYWORDS = [
        "meeting", "schedule", "review", "reply", "respond",
        "confirm", "discussion", "approve", "approval",
        "request", "deadline", "feedback", "update",
        "call", "connect", "availability"
    ]

    NOTIFY_KEYWORDS = [
        "bank", "otp", "password", "security", "account",
        "transaction", "login", "unauthorized", "alert",
        "suspicious", "verify", "verification", "breach",
        "payment", "credit card", "debit", "kyc"
    ]

    # 🔥 PRIORITY MATTERS (SECURITY FIRST)
    for word in NOTIFY_KEYWORDS:
        if word in email:
            state["triage_decision"] = "notify_human"
            state["reasoning"] = "Security or sensitive email detected"
            return state

    for word in RESPOND_KEYWORDS:
        if word in email:
            state["triage_decision"] = "respond"
            state["reasoning"] = "Action or reply required"
            return state

    for word in IGNORE_KEYWORDS:
        if word in email:
            state["triage_decision"] = "ignore"
            state["reasoning"] = "Promotional or marketing email"
            return state

    # Default safe fallback
    state["triage_decision"] = "notify_human"
    state["reasoning"] = "Uncertain content – human review required"
    return state