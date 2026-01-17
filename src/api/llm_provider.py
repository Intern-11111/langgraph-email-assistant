import os

from dotenv import load_dotenv

load_dotenv()

# Single global instance cache
LLM_INSTANCE = None


def get_llm():
    global LLM_INSTANCE
    if LLM_INSTANCE is not None:
        return LLM_INSTANCE

    provider = os.getenv("LLM_PROVIDER", "huggingface")

    # =====================================================
    # OPTION 1 — OpenRouter (Preferred: LLaMA 3.3 70B)
    # =====================================================
    if provider == "openrouter":
        print("🔌 Using OpenRouter LLM Provider")

        from langchain_openai import ChatOpenAI

        # ✅ Best free OpenRouter model for JSON + drafting
        model_name = os.getenv(
            "OPENROUTER_MODEL",
            "meta-llama/llama-3.3-70b-instruct:free",
        )

        LLM_INSTANCE = ChatOpenAI(
            model=model_name,
            temperature=0.2,
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            default_headers={
                "HTTP-Referer": "https://github.com/Intern-11111/langgraph-email-assistant",
                "X-Title": "LangGraph Email Agent",
            },
            # Do NOT force response_format here
            # Some OpenRouter models error if this is set
        )

        return LLM_INSTANCE
    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")
