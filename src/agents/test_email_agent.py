from agents.react_loop import ReactAgent


def email_agent_callable(inputs: dict) -> dict:
    """
    LangSmith-compatible agent callable.
    Accepts a dict with keys like 'subject', 'body', 'sender'.
    Returns a dict containing a 'response' key for evaluation.
    """
    email_subject = inputs.get("subject", "")
    email_body = inputs.get("body", "")
    sender = inputs.get("sender")

    agent = ReactAgent(max_steps=6)
    result = agent.run(email_subject, email_body, context={"sender": sender} if sender else {})

    # Provide the final summary as the primary response for judging.
    final = result.get("final", {})
    summary = final.get("summary") if isinstance(final, dict) else None
    response_text = summary or "Agent processed email and produced a result."

    return {
        "response": response_text,
        "trace": result,
    }


def email_agent_chain():
    """Factory function returning the callable chain for LangSmith run_on_dataset."""
    return email_agent_callable
