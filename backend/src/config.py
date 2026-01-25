from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def gemini_ai_model()->ChatGoogleGenerativeAI:
    """
    Creates a connection to Google's Gemini AI model.
    This is what powers the email classification and reply generation.
    """
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Error: GOOGLE_API_KEY not found in environment.")
    
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
    )
    print("LLM ready!")
    return model