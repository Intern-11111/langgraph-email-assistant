# langgraph-email-assistant
"Building an Ambient Agent with LangGraph for an Email Assistant"
<br>
Intelligent ambient agent leveraging LangGraph to process, analyze, and automate email workflows with real-time assistance and proactive insights.

# Ambient Email Agent with LangGraph

Stateful, ambient email assistant built with **LangGraph**, **LangChain**, **Gemini (Google GenAI)** and optionally **Hugging Face** models, plus **LangSmith** for tracing and evaluation.

---

## 1. Environment Setup

### 1.1. Python & Virtual Env

python3.11 -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt


---

## 2. Environment Variables

Create a `.env` file in the project root:

===== LLM PROVIDERS =====
Google Gemini (Google GenAI)
GOOGLE_API_KEY=your_gemini_api_key_here

Hugging Face (optional provider)
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here

===== LangSmith (Tracing & Evaluation) =====
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=ambient-email-agent

===== Gmail / Calendar (used later) =====
GMAIL_CLIENT_ID=your_gmail_oauth_client_id
GMAIL_CLIENT_SECRET=your_gmail_oauth_client_secret
GMAIL_REFRESH_TOKEN=your_gmail_refresh_token

===== General =====
ENV=dev


> Never commit `.env` to Git. Add it to `.gitignore`.

---

## 3. LLM Setup

LLMs are configured in `src/config.py`. This project supports:

- **Primary**: Google Gemini via `langchain-google-genai`
- **Optional**: Hugging Face models via `langchain` integrations

### 3.1. Gemini (Google GenAI) Client

src/config.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_gemini_llm() -> ChatGoogleGenerativeAI:
return ChatGoogleGenerativeAI(
model="gemini-2.0-flash-exp", # or another Gemini model
google_api_key=os.getenv("GOOGLE_API_KEY"),
temperature=0.3,
)


### 3.2. Hugging Face LLM (Optional)

You can also plug in a Hugging Face chat model for local/alternative experiments:

src/config.py (continued)
from langchain.chat_models import ChatOpenAI
from langchain_huggingface import ChatHuggingFace

def get_hf_llm() -> ChatHuggingFace:
# Example: use a Hugging Face Inference Endpoint or hosted model
return ChatHuggingFace(
repo_id="mistralai/Mistral-7B-Instruct-v0.3", # change to your model
huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
temperature=0.3,
)


> In the rest of the project, use a small factory function (e.g. `get_llm(provider="gemini")`) so you can switch providers without changing all nodes.

---

## 4. Datasets

The project uses **small, curated email datasets** for triage and evaluation, stored in the `data/` folder.

### 4.1. Triage Test Set (Milestone 1)

File: `data/test_emails.csv`

Used to measure **triage accuracy** on 25–50 examples.

**Schema (CSV):**

id,subject,body,label,ideal_response
1,"Meeting tomorrow?","Hi, can we meet at 3pm tomorrow? Thanks!","respond_act","Confirm 3pm, ask for agenda"
2,"Newsletter: Weekly Update","This week we shipped X, Y, Z...","ignore",""
3,"Urgent: Server down","Production server crashed NOW","notify_human","Flag for immediate human review"


- `label` is one of: `ignore`, `notify_human`, `respond_act`
- `ideal_response` is a short description of what a good agent reply / behavior should be

### 4.2. Evaluation Dataset (Milestone 2+)

File: `data/eval_dataset.jsonl` (recommended) or `data/eval_dataset.json`

Each line is a JSON object representing one test case for LangSmith:

{
"id": "email_001",
"subject": "Need confirmation for Friday meeting",
"body": "Hi, can you confirm if we are still on for Friday at 3 PM?",
"label": "respond_act",
"ideal_response": "Confirm Friday 3 PM, polite tone, ask if any agenda items."
}

text

- Target size: **100+** labeled examples.
- Upload this file as a **Dataset** in LangSmith for automated evaluation.

### 4.3. Creating Your Own Dataset

- Start with manually written or anonymized emails that reflect your real use cases.
- Label each with:
  - `label` (`ignore` / `notify_human` / `respond_act`)
  - `ideal_response` description
- Keep the dataset small but high‑quality at first; you can expand later.

---

## 5. Running Basic Checks

### 5.1. Test LLM Connectivity

python -m src.sanity_check_llm

text

Example `src/sanity_check_llm.py`:

from config import get_gemini_llm

if name == "main":
llm = get_gemini_llm()
resp = llm.invoke("Say hello from the ambient email agent project.")
print(resp)

text

### 5.2. Explore Datasets in a Notebook

jupyter lab notebooks/

text

In a notebook, you can load and inspect:

import pandas as pd

df = pd.read_csv("data/test_emails.csv")
df.head()

text

---

You can extend this `README.md` later with sections for:

- Graph diagram of the LangGraph workflow
- HITL (Human-in-the-Loop) setup
- Deployment with FastAPI / Streamlit