
import os
from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="models/gemini-2.5-flash",
#     temperature=0,
#     api_key=os.getenv("GOOGLE_API_KEY")
# )

# triage.py

SENSITIVE_KEYWORDS = [
    "send",
    "reply",
    "forward",
    "delete",
    "resign",
    "quit",
    "urgent"
]

IGNORE_KEYWORDS = ["newsletter", "promotion", "unsubscribe", "sale"]
NOTIFY_KEYWORDS = ["invoice", "payment", "alert", "warning"]
RESPOND_KEYWORDS = ["reply", "respond", "meeting", "schedule", "urgent", "send"]

def triage_node(state):
    text = f"{state.get('subject', '')} {state.get('body', '')}".lower()

    for w in IGNORE_KEYWORDS:
        if w in text:
            state["category"] = "ignore"
            state["intent"] = None
            state["requires_approval"] = False
            return state

    for w in NOTIFY_KEYWORDS:
        if w in text:
            state["category"] = "notify_human"
            state["intent"] = None
            state["requires_approval"] = False
            return state

    for w in RESPOND_KEYWORDS:
        if w in text:
            state["category"] = "respond"
            state["intent"] = "send_email"
            state["requires_approval"] = True
            return state

    state["category"] = "ignore"
    state["intent"] = None
    state["requires_approval"] = False
    return state
