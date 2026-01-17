import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Import routers
from src.api.router import router as triage_router
from src.api.huggingface_router import router as hf_router
from src.api.eval_router import router as eval_router
from src.api.debug_router import router as debug_router
# ADD THIS
from src.integrations.gmail_webhook import router as gmail_router

app = FastAPI(
    title="Ambient Email Agent",
    description="A LangGraph-powered email assistant with LangChain integration, persistent memory, and real-time webhook support for Gmail automation",
    version="1.0.0",
)

# ----------------- APP INITIALIZATION -----------------
app.include_router(eval_router, prefix="/eval", tags=["Evaluation"])

# ADD THIS (NO PREFIX)
app.include_router(gmail_router, tags=["Gmail"])
app.include_router(debug_router)

# ----------------- CORS SETTINGS -----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        "available_endpoints": {
            "triage_email": "/triage/email",
            "gmail_webhook": "/gmail/webhook",  # ✅ NOW REAL
        },
    }
