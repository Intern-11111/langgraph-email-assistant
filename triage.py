# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="models/gemini-2.5-flash",
#     temperature=0,
#     api_key=os.getenv("GOOGLE_API_KEY")
# )

# def triage_node(state):
#     email = state["email"]

#     prompt = f"""
#     You are an email assistant.
#     Classify the email into one category:
#     - ignore
#     - notify_human
#     - respond

#     Email:
#     {email}

#     Return only one word.
#     """

#     try:
#         response = llm.invoke(prompt)
#         decision = response.content.strip().lower()

#         if decision not in ["ignore", "notify_human", "respond"]:
#             decision = "notify_human"

#     except Exception:
#         decision = "notify_human"

#     return {
#         **state,
#         "category": decision
#     }
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    temperature=0,
    api_key=os.getenv("GOOGLE_API_KEY")
)

def triage_node(state):
    email_text = state["email"].lower()

    # ---------- RULE-BASED DECISIONS (FAST & CLEAR) ----------

    IGNORE_KEYWORDS = [
        "newsletter", "no action required", "promotion",
        "weekly update", "terms and conditions", "welcome to"
    ]

    RESPOND_KEYWORDS = [
        "can we", "please confirm", "schedule", "meeting",
        "let me know", "kindly", "request"
    ]

    NOTIFY_KEYWORDS = [
        "urgent", "security", "account", "password",
        "unauthorized", "alert", "suspicious"
    ]

    # Ignore rules
    if any(word in email_text for word in IGNORE_KEYWORDS):
        decision = "ignore"

    # Notify human rules
    elif any(word in email_text for word in NOTIFY_KEYWORDS):
        decision = "notify_human"

    # Respond rules
    elif any(word in email_text for word in RESPOND_KEYWORDS):
        decision = "respond"

    # ---------- LLM FALLBACK (ONLY IF UNCLEAR) ----------
    else:
        prompt = f"""
        Classify the email into one action:
        - ignore
        - notify_human
        - respond

        Email:
        {state['email']}

        Return only one word.
        """

        try:
            response = llm.invoke(prompt)
            decision = response.content.strip().lower()

            if decision not in ["ignore", "notify_human", "respond"]:
                decision = "notify_human"

        except Exception:
            decision = "notify_human"

    return {
        **state,
        "category": decision
    }
