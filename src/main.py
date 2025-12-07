import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
os.environ.setdefault("LANGCHAIN_PROJECT", "langgraph-email-assistant")
if os.getenv("LANGSMITH_API_KEY") and not os.getenv("LANGCHAIN_API_KEY"):
    langsmith_key = os.getenv("LANGSMITH_API_KEY")
    if langsmith_key:
        os.environ["LANGCHAIN_API_KEY"] = langsmith_key

from agents.hello_agent import hello_agent


def main():
    try:
        response = hello_agent()
        print("Agent response:", response)
    except Exception as e:
        # Provide a concise error message for missing configuration or runtime issues
        print("Error running agent:", e)


if __name__ == "__main__":
    main()
