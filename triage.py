import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
#os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    #temperature=0,
    api_key=os.getenv("GOOGLE_API_KEY")
    #api_key="AIzaSyBGI58CgbhBm4kR4Vbc0ZREhgYb7-X7fbs"  # reads from .env automatically
)

def triage_email(email: str) -> str:
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

    response = llm.invoke(prompt)
    return response.content.strip().lower()
