
from typing import Dict, Any
from .triage_llm import LLMFallbackTriage
from .triage_rules import RuleBasedTriage

class TriageNode:
    """
    Triage Node for LangGraph.
    Final outputs:
        - ignore
        - notify_human
        - reason_act
    """

    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
        self.rules = RuleBasedTriage()
        self.llm = LLMFallbackTriage()

    def run(self, email):
        subject = email.get("subject", "")
        body = email.get("body", "")
        sender = email.get("sender", "")

        rule_result = self.rules.classify(subject, body, sender)

        # RULES WIN IF CONFIDENT
        if rule_result["confidence"] >= self.threshold:
            return {
                "final_label": rule_result["label"].strip().lower(),
                "final_confidence": rule_result["confidence"],
                "source": "rules"
            }

        # LLM FALLBACK
        llm_result = self.llm.classify(subject, body)

        return {
            "final_label": llm_result["label"].strip().lower(),
            "final_confidence": llm_result["confidence"],
            "source": "llm"
        }

    def triage_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        email = state.get("email_text", {})
        state["triage_result"] = self.run(email)
        return state

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return self.triage_node(state)
