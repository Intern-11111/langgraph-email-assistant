"""
Configuration module for the email agent.
Hybrid: LLM for Triage, Templates for Response.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_config():
    """
    Get application configuration.
    """
    config = {
        "db_path": os.getenv("DB_PATH", "data/checkpoints.db"),
        "mock_mode": True
    }
    return config

def gemini_ai_model() -> ChatGoogleGenerativeAI:
    """
    Creates a connection to Google's Gemini AI model.
    Used for intelligent email triage.
    """
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Error: GOOGLE_API_KEY not found in environment.")
    
    # Use flash-lite for speed and cost effectiveness
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
    )
    print("LLM (Gemini) ready for triage.")
    return model