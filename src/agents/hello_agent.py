import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

# Load environment variables from .env if present
load_dotenv()

# Optional: LangSmith tracing setup (uses env vars if available)
os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
os.environ.setdefault("LANGCHAIN_PROJECT", "langgraph-email-assistant")
if os.getenv("LANGSMITH_API_KEY") and not os.getenv("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")


def _get_llm() -> ChatOpenAI:
    """Create and return a ChatOpenAI client using environment configuration."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing OPENAI_API_KEY in environment. Set it in .env or system env."
        )
    return ChatOpenAI(model="gpt-4o-mini", api_key=SecretStr(api_key))


def hello_agent() -> str:
    llm = _get_llm()
    msg = llm.invoke("Hello, I am testing my agent setup.")
    # `invoke` returns an AIMessage; extract the text content
    return getattr(msg, "content", str(msg))


if __name__ == "__main__":
    print("Agent response:", hello_agent())
