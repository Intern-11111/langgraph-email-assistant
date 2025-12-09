from triage.triage_rules import RuleBasedTriage
from triage.triage_llm import LLMFallbackTriage


class TriageNode:

    def __init__(self, threshold=0.80):
  
        #threshold: minimum confidence score to trust rules
   
        self.threshold = threshold
        self.rules = RuleBasedTriage()
        self.llm = LLMFallbackTriage()

    # LangGraph calls this method
    def run(self, email):
        """
        email = {
            "subject": "...",
            "body": "...",
            "sender": "...",
            "attachments": [...],   # optional
        }

        Returns:
        {
            "final_label": "...",
            "final_confidence": 0.xx,
            "source": "rules" or "llm"
        }
        """

        subject = email.get("subject", "")
        body = email.get("body", "")
        sender = email.get("sender", "")

        # 1️Run rule-based triage
        rule_result = self.rules.classify(subject, body, sender)
        rule_label = rule_result["label"]
        rule_conf = rule_result["confidence"]

        # If rules are confident → use them
        if rule_conf >= self.threshold:
            return {
                "final_label": rule_label,
                "final_confidence": rule_conf,
                "source": "rules"
            }

        # Else → Fallback to LLM
        llm_result = self.llm.classify(subject, body)

        return {
            "final_label": llm_result["label"],
            "final_confidence": llm_result["confidence"],
            "source": "llm"
        }


if __name__ == "__main__":
    triage = TriageNode()

    sample_email = {
        "subject": "Can we schedule a meeting?",
        "body": "Let me know when you're free.",
        "sender": "boss@company.com"
    }

    print(triage.run(sample_email))
