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
    email = state["email"]

    prompt = f"""
    You are an email assistant.
    Classify the email into one category:
    - ignore
    - notify_human
    - respond

    Email:
    {email}

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
