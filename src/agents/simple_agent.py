from langchain_openai import ChatOpenAI
from utils.config import OPENAI_API_KEY, require_env


def _get_llm() -> ChatOpenAI:
    require_env("OPENAI_API_KEY", OPENAI_API_KEY)
    return ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)


def simple_agent() -> str:
    llm = _get_llm()
    msg = llm.invoke("Hello! Respond with: Hello Agent works!")
    return getattr(msg, "content", str(msg))