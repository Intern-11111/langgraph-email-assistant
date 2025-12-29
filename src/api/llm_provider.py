import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_community.llms import HuggingFacePipeline

# ---------- GLOBAL MODEL CACHE (to avoid re-loading on every request) ----------
LLM_MODEL = None


def load_local_hf_model():
    """Load the model once and reuse for all requests."""
    global LLM_MODEL
    if LLM_MODEL is not None:
        return LLM_MODEL

    model_name = os.getenv("HF_MODEL", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    print(f" Loading HuggingFace Model: {model_name}")
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

    LLM_MODEL = HuggingFacePipeline(pipeline=gen_pipe)
    print("Model loaded and ready!")
    return LLM_MODEL


def get_llm():
    """Public accessor for the model"""
    return load_local_hf_model()
