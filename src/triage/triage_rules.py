import re

class TriageRules:

    def __init__(email):
        email.spam_keywords = [
            "win money", "you won", "lottery", "claim now", "urgent",
            "100% free", "urgent prize"
        ]

        email.promotion_keywords = [
            "sale", "discount", "offer", "deal", "promotion",
            "unsubscribe", "buy now"
        ]

        email.finance_keywords = [
            "invoice", "payment due", "bill", "receipt",
            "transaction", "bank", "account update", "account",
            "security alert", "suspicious login", "login attempt"
        ]

        
        email.meeting_keywords = [
            "meeting", "zoom", "call", "appointment", "calendar", "invite",
            "reschedule", "teams"
        ]

       
        email.job_keywords = [
            "interview", "hiring", "opportunity", "resume", "shortlisted", "internship",
            "job application", "position", "career", "vacancy"
        ]

        email.transactional_keywords = [
            "your order", "order ", "shipped", "tracking number",
            "delivery", "delivered", "package"
        ]

        email.personal_keywords = [
            "hey", "congrats", "congratulations", "alumni", "meetup",
            "lunch", "are you free", "wishing you", "tomorrow?", "friendly reminder"
        ]

    def contains_keyword(email, text, keywords):
        text = text.lower()
        return any(kw in text for kw in keywords)

    def _keyword_confidence(email, text, keywords):
        text = text.lower()
        matches = sum(1 for kw in keywords if kw in text)
        if matches == 0:
            return 0.0
        # Discrete, interpretable confidence
        return 1.0 if matches >= 3 else (0.8 if matches == 2 else 0.6)

    def classify(email, subject, body, sender=""):

        full_text = f"{subject} {body}".lower()

        #Automated if sender is clearly no-reply
        if "noreply" in sender.lower():
            return {
                "label": "automated",
                "source": "rule",
                "confidence": 1.0
            }

        if email.contains_keyword(full_text, email.spam_keywords):
            return {
                "label": "spam",
                "source": "rule",
                "confidence": email._keyword_confidence(full_text, email.spam_keywords)
            }

        if email.contains_keyword(full_text, email.promotion_keywords):
            return {
                "label": "promotion",
                "source": "rule",
                "confidence": email._keyword_confidence(full_text, email.promotion_keywords)
            }

        if email.contains_keyword(full_text, email.finance_keywords):
            return {
                "label": "finance",
                "source": "rule",
                "confidence": email._keyword_confidence(full_text, email.finance_keywords)
            }

        if email.contains_keyword(full_text, email.meeting_keywords):
            return {
                "label": "meeting",
                "source": "rule",
                "confidence": email._keyword_confidence(full_text, email.meeting_keywords)
            }
        
        if email.contains_keyword(full_text, email.job_keywords):
            return {
                "label": "job_related",
                "source": "rule",
                "confidence": email._keyword_confidence(full_text, email.job_keywords)
            }

        if email.contains_keyword(full_text, email.transactional_keywords):
            return {
                "label": "transactional",
                "source": "rule",
                "confidence": email._keyword_confidence(full_text, email.transactional_keywords)
            }

        if email.contains_keyword(full_text, email.personal_keywords):
            return {
                "label": "personal",
                "source": "rule",
                "confidence": email._keyword_confidence(full_text, email.personal_keywords)
            }

        return {
            "label": "uncertain",
            "source": "rule",
            "confidence": 0.0
        }

if __name__ == "__main__":
    triage = TriageRules()

    email_subject = "🔥 50% discount just for you!"
    email_body = "Hurry up! Buy now and save money."
    sender = "promo@shopping.com"

    result = triage.classify(email_subject, email_body, sender)
    print("Rule-based result:", result)
    RuleBasedTriage = TriageRules
