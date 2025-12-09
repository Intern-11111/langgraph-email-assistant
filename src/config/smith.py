import os

# This file centralizes LangSmith configuration.
# Safe to import even if LangSmith is not configured.

def is_langsmith_enabled() -> bool:
    """
    Returns True if LangSmith tracing is enabled via env vars.
    """
    return (
        os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
        and os.getenv("LANGCHAIN_API_KEY") is not None
    )


def get_project_name(default: str = "Email-Triage-Agent") -> str:
    """
    Returns the LangSmith project name.
    """
    return os.getenv("LANGCHAIN_PROJECT", default)
