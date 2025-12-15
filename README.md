# 🚀 LangGraph Email Assistant  
### *Building an Ambient Agent with LangGraph for Intelligent Email Automation*

An **intelligent ambient agent** built using **LangGraph** to process, analyze, and automate email workflows with **real-time assistance** and **proactive AI-driven insights**.

---

## 🎯 Milestone 1 Goal

The primary objective of **Milestone 1** was to establish a **strong technical foundation** for the email assistant system by:

- ⚙️ Setting up a robust development environment  
- 🗂️ Defining a scalable project structure  
- 🤖 Validating core AI and LLM frameworks  
- 🧪 Implementing **HelloAgent** (Initial LangGraph Proof-of-Concept)  
- 🔄 Demonstrating an end-to-end working pipeline  

---

## ✅ What Was Done in Milestone 1

### 🔧 Environment & Infrastructure *(Lead Responsibility)*

- Created and validated a **Python virtual environment**
- Installed and locked all required dependencies
- Configured `.gitignore` to exclude:
  - `venv/`
  - `.env`
  - cache and temporary files
- 🔐 **API Configuration**:
  - Configured `.env` to securely manage the **Gemini API Key**  
  - Environment variable used: `GOOGLE_API_KEY`
- Designed a **clean and scalable repository structure** for future milestones

---

### 📦 Dependency Validation

The following libraries were installed, tested, and confirmed working successfully:

- `langchain`
- `langgraph`
- `langchain-google-genai` *(Gemini integration)*
- `transformers`
- `datasets`
- `fastapi`
- `uvicorn`

---

### 🤖 Core Functionality – HelloAgent

- Implemented **HelloAgent**, a foundational **LangGraph-based agent**
- Integrated **Google Gemini** via LangChain
- Validated:
  - Graph state execution
  - LLM connectivity
  - Proper API communication flow

✅ **HelloAgent Validation Result**:  
Successful API handshake and response generation using Google’s Gemini models.

---

## 🗂️ Project Structure

```plaintext
langgraph-email-assistant/
├── src/                  # Core application and agent logic
├── agents/               # Contains hello_agent.py and triage logic
├── run_server.py         # FastAPI server entry point
├── requirements.txt      # Python dependencies
├── README.md             # Project overview and documentation
├── env_setup.md          # Environment setup guide
└── .gitignore            # Ignore venv, .env, and cache files
