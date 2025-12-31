def get_judge_questions(response_text):
    return {
        "helpfulness": f"""
Rate the helpfulness (1-5) of the following response:
{response_text}
""",
        "accuracy": f"""
Rate the accuracy (1-5) of the following response:
{response_text}
""",
        "tone": f"""
Rate the tone (1-5) of the following response:
{response_text}
"""
    }
