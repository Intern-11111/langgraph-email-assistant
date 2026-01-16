def email_agent(state):
    user_input = state.get("input", "No user input provided")

    email_draft = {
        "to": "hr@company.com",
        "subject": "Intern Application",
        "body": user_input
    }

    return {
        "email_data": email_draft
    }
