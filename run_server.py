import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Import routers (aliasing for safety)
from src.api.router import router as triage_router
from src.api.huggingface_router import router as hf_router

app = FastAPI(
    title="Ambient Email Agent – Milestone 1",
    description="Email Triage using FREE Local HuggingFace Models",
    version="1.0.0",
)

# ----------------- CORS SETTINGS -----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # tighten later for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- ROUTES REGISTER -----------------
app.include_router(triage_router, prefix="/triage", tags=["Triage"])
app.include_router(hf_router, prefix="/huggingface", tags=["HuggingFace"])

# ----------------- ROOT HEALTH CHECK -----------------
@app.get("/")
def health():
    return {
        "status": "online",
        "llm_provider": os.getenv("LLM_PROVIDER", "huggingface"),
        "hf_model": os.getenv(
            "HF_MODEL",
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        ),
        "available_endpoints": {
            "triage_email": "/triage/email",
            "huggingface_data": "/huggingface/data?limit=10",
            "huggingface_triage": "/huggingface/triage?limit=10",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "run_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
