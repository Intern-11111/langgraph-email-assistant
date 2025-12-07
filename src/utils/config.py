import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

def require_env(key: str, val: str):
    if not val:
        raise EnvironmentError(f"Environment variable {key} is not set. Please copy .env.sample -> .env and fill it.")