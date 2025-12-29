
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

    def run(self, email: Dict[str, Any]):
        subject = email.get("subject", "")
        body = email.get("body", "")
        sender = email.get("sender", "")

        rb = self.rules.classify(subject, body, sender)

        if rb["confidence"] >= self.threshold:
            return {
                "final_label": rb["label"],
                "final_confidence": rb["confidence"],
                "source": "rules"
            }

        llm = self.llm.classify(subject, body)

        return {
            "final_label": llm["label"],
            "final_confidence": llm["confidence"],
            "source": "llm"
        }

    def triage_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        email = state.get("email_text", {})
        state["triage_result"] = self.run(email)
        return state

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return self.triage_node(state)
