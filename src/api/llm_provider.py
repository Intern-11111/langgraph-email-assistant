import os
import torch
from dotenv import load_dotenv

load_dotenv()

# Single global instance cache
LLM_INSTANCE = None


def get_llm():
    global LLM_INSTANCE
    if LLM_INSTANCE is not None:
        return LLM_INSTANCE

    provider = os.getenv("LLM_PROVIDER", "huggingface")

    
    #   OPTION 1 — OpenRouter (preferred for accuracy)
   
    if provider == "openrouter":
        print("🔌 Using OpenRouter LLM Provider")

        from langchain_openai import ChatOpenAI

        model_name = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-r1-0528:free")

        LLM_INSTANCE = ChatOpenAI(
            model=model_name,
            temperature=0.2,
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            default_headers={
                "HTTP-Referer": "https://github.com/Intern-11111/langgraph-email-assistant",
                "X-Title": "LangGraph Email Agent",
            },
        )
        return LLM_INSTANCE

   
    #   OPTION 2 — Free Local HuggingFace Pipeline
    
    if provider == "huggingface":
        print(" Using Local HuggingFace Model")

        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
        from langchain_community.llms import HuggingFacePipeline

        model_name = os.getenv("HF_MODEL", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        device = 0 if torch.cuda.is_available() else -1

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if device == 0 else torch.float32
        )

        gen_pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=128,
            temperature=0.2,
            device=device
        )

        LLM_INSTANCE = HuggingFacePipeline(pipeline=gen_pipe)
        return LLM_INSTANCE
    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")

