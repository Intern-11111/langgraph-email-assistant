import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

def run_hello_agent():
    print("--- 🚀 Initializing 'Hello Agent' Test ---")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found.")
        return

    try:
        print("Connecting to Google Gemini...")

        llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash"   # ✅ WORKING MODEL
        )

        prompt = "Hello! Briefly explain what an 'Ambient Agent' is in one sentence."
        response = llm.invoke([HumanMessage(content=prompt)])

        print("✅ SUCCESS!")
        print("--------------------------------------------------")
        print(response.content)
        print("--------------------------------------------------")

    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    run_hello_agent()
