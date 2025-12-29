# from tools import read_calendar

# def react_agent(email: str):
#     thoughts = []

#     thoughts.append("Thinking about the email...")

#     if "meeting" in email.lower():
#         thoughts.append("Need to check calendar")
#         calendar_info = read_calendar()
#         thoughts.append(calendar_info)

#         reply = f"Sure, I am available. {calendar_info}"
#         return reply, thoughts

#     return "No action needed", thoughts

from tools import read_calendar

# def react_agent(email: str):
#     thoughts = []

#     thoughts.append("Thinking about the email...")

#     if "meeting" in email.lower():
#         thoughts.append("Need to check calendar")
#         calendar_info = read_calendar()
#         thoughts.append(calendar_info)

#         reply = f"Sure, I am available. {calendar_info}"
#         return reply, thoughts

#     return "No action needed", thoughts

# def agent_node(state):
#     email = state["email"]

#     thoughts = [
#         "Read the email",
#         "Understand user intent",
#         "Prepare a polite professional reply"
#     ]

#     reply = "Sure, I’m available tomorrow afternoon."

#     return {
#         **state,
#         "thoughts": thoughts,
#         "reply": reply
#     }

def agent_node(state):
    thoughts = [
        "Email requires a response",
        "Understanding user intent",
        "Drafting professional reply"
    ]

    reply = "Sure, I’m available tomorrow afternoon."

    return {
        **state,
        "thoughts": thoughts,
        "reply": reply
    }
