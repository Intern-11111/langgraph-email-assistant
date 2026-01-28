import re


SPAM_KEYWORDS = [
    r"free\b",
    r"win\b",
    r"offer\b",
    r"discount\b",
    r"deal\b",
    r"promo\b",
]

DANGEROUS_KEYWORDS = [
    r"password",
    r"otp",
    r"bank",
    r"verify",
    r"urgent",
    r"click\s+here",
]


def classify_email_overall(snippet: str, subject: str, body: str, sender: str) -> str:
    """Simple heuristic classifier: returns 'dangerous', 'spam', or 'safe'.

    - dangerous: contains phishing/security-critical keywords
    - spam: promotional keywords
    - safe: otherwise
    """
    text = " ".join([snippet or "", subject or "", body or "", sender or ""]).lower()

    for pat in DANGEROUS_KEYWORDS:
        if re.search(pat, text):
            return "dangerous"

    for pat in SPAM_KEYWORDS:
        if re.search(pat, text):
            return "spam"

    return "safe"
