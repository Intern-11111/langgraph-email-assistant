import os
from dotenv import load_dotenv
from langsmith import traceable

# Load environment variables
load_dotenv()

print("Tracing enabled:", os.getenv("LANGCHAIN_TRACING_V2"))
print("LangSmith project:", os.getenv("LANGCHAIN_PROJECT"))
print("API key loaded:", os.getenv("LANGSMITH_API_KEY") is not None)

"""
Milestone 3 – HITL Pause and Safety Test

This file is not a full agent implementation.
It is only used to test whether:
1. Dangerous actions are detected
2. HITL pause is triggered
3. LangSmith captures the full decision flow
"""

@traceable
def decide_action_type(email_text):
    """
    This function simulates how the agent
    classifies an email before taking action.
    """
    if "refund" in email_text.lower():
        return "dangerous"
    if "account" in email_text.lower():
        return "dangerous"
    return "safe"


@traceable
def hitl_decision(action_type):
    """
    This function simulates the HITL checkpoint.
    If the action is dangerous, the system pauses.
    """
    if action_type == "dangerous":
        print("HITL PAUSE: Waiting for human approval")
        return "paused_for_review"
    else:
        print("Action is safe. Continuing execution")
        return "continue_execution"


@traceable
def full_hitl_flow(email_text):
    """
    This function represents the complete
    decision flow of the agent for one email.
    It acts as the parent trace.
    """
    action_type = decide_action_type(email_text)
    final_state = hitl_decision(action_type)
    return final_state


def run_milestone3_test():
    """
    This test runs one example email through
    the full simulated HITL flow.
    """
    test_email = "Customer is requesting a refund for a recent purchase"

    final_state = full_hitl_flow(test_email)

    print("Test Email:", test_email)
    print("Final System State:", final_state)


if __name__ == "__main__":
    run_milestone3_test()
