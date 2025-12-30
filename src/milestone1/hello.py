import os
import argparse
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
    parser = argparse.ArgumentParser(description="Run the hello agent")
    parser.add_argument("--prompt", type=str, help="Custom prompt to send to the agent", default=None)
    args = parser.parse_args()

    try:
        print("Running agent...")
        response = hello_agent(prompt=args.prompt)
        print("Agent response:", response)
    except Exception as e:
        # Provide a concise error message for missing configuration or runtime issues
        print("Error running agent:", e)


if __name__ == "__main__":
    main()
