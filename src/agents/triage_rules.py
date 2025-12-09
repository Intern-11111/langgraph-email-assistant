import re

class TriageRules:

    def __init__(email):
        email.spam_keywords = [
            "win money", "you won", "lottery", "claim now", "urgent",
            "100% free", "click here", "urgent prize"
        ]

        email.promotion_keywords = [
            "sale", "discount", "offer", "deal", "promotion",
            "unsubscribe", "buy now"
        ]

        email.finance_keywords = [
            "invoice", "payment due", "bill", "receipt",
            "transaction", "bank", "account update"
        ]

        email.meeting_keywords = [
            "meeting", "schedule", "zoom", "call", "appointment" , "calendar", "invite", 
            "reminder" , "reschedule" , "Teams"
        ]

        email.job_keywords = [
            "interview", "hiring", "opportunity", "resume", "shortlisted", "internship",
            "job application" , "position" , "career" , "vacancy" , "role"
        ]

        email.transactional_keywords = [
            "your order", "shipped", "tracking number",
            "delivery", "package"
        ]

    def contains_keyword(email, text, keywords):
        text = text.lower()
        return any(kw in text for kw in keywords)

    def classify(email, subject, body, sender=""):

        full_text = f"{subject} {body}".lower()

        if email.contains_keyword(full_text, email.spam_keywords):
            return {
                "label": "spam",
                "source": "rule"
            }

        if email.contains_keyword(full_text, email.promotion_keywords):
            return {
                "label": "promotion",
                "source": "rule"
            }

        if email.contains_keyword(full_text, email.finance_keywords):
            return {
                "label": "finance",
                "source": "rule"
            }

        if email.contains_keyword(full_text, email.meeting_keywords):
            return {
                "label": "meeting",
                "source": "rule"
            }
        
        if email.contains_keyword(full_text, email.job_keywords):
            return {
                "label": "job_related",
                "source": "rule"
            }

        if email.contains_keyword(full_text, email.transactional_keywords):
            return {
                "label": "transactional",
                "source": "rule"
            }

        if "noreply" in sender.lower():
            return {
                "label": "automated",
                "source": "rule"
            }

        return {
            "label": "uncertain",
            "source": "rule"
        }

if __name__ == "__main__":
    triage = TriageRules()

    email_subject = "🔥 50% discount just for you!"
    email_body = "Hurry up! Buy now and save money."
    sender = "promo@shopping.com"

    result = triage.classify(email_subject, email_body, sender)
    print("Rule-based result:", result)
