from tools import read_calendar

def react_agent(email: str):
    thoughts = []

    thoughts.append("Thinking about the email...")

    if "meeting" in email.lower():
        thoughts.append("Need to check calendar")
        calendar_info = read_calendar()
        thoughts.append(calendar_info)

        reply = f"Sure, I am available. {calendar_info}"
        return reply, thoughts

    return "No action needed", thoughts
