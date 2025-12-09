import os
import torch

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "huggingface")  # default = free local

    # ---------- Paid providers (optional, if you ever use them) ----------
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-4.1-mini", temperature=0.2)

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

    # ------------------- FREE LOCAL HUGGINGFACE MODEL --------------------
    # Choose a SMALL model suitable for 8GB RAM:
    #   - TinyLlama/TinyLlama-1.1B-Chat-v1.0   (good)
    #   - google/gemma-2-2b-it                 (ok, heavier)
    model_name = os.getenv("HF_MODEL", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
    from langchain_community.llms import HuggingFacePipeline

    device = 0 if torch.cuda.is_available() else -1  # GPU if present, else CPU

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

    return HuggingFacePipeline(pipeline=gen_pipe)
