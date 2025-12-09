# langgraph-email-assistant

This repository contains **Milestone 1** of an Ambient Email Assistant built using **LangGraph**, **LangChain**, and **Hugging Face Transformers**.

Milestone 1 focuses on **environment setup, infrastructure readiness, and a basic email triage agent**.

---

##  Milestone 1 Goal

Establish a solid foundation for the email assistant by:
- Setting up the development environment
- Defining the project structure
- Validating core AI frameworks
- Implementing a basic triage agent
- Demonstrating the system end-to-end

---

##  What Was Done in Milestone 1

### 🔧 Environment & Infrastructure (Lead Responsibility)
- Created and validated Python virtual environment
- Installed and locked all required dependencies
- Configured `.gitignore` to exclude `venv/` and `.env`
- Structured the repository for scalability

###  Dependency Validation
The following libraries were installed and confirmed working:
- `langchain`
- `langgraph`
- `huggingface transformers`
- `datasets`
- `fastapi`
- `uvicorn`

###  Core Functionality – Email Triage Agent
Implemented a **LangGraph-based agent** that classifies incoming emails into:

- **ignore** → spam / marketing / irrelevant
- **notify_human** → ambiguous or sensitive emails
- **respond** → safe for autonomous reply

The agent consists of:
1. **Triage Node** – heuristic-based decision logic
2. **ReAct Node** – drafts a reply when action is `respond`

###  Evaluation & Demo
- Integrated Hugging Face’s `SetFit/enron_spam` dataset
- Built evaluation endpoints to compare predictions vs ground truth
- Measured strict 3-way classification accuracy
- Verified system behavior through API demos

---

##  Project Structure

```text
langgraph-email-assistant/
├── src/                  # Core application and agent logic
├── data/                 # Dataset and evaluation utilities
├── run_server.py         # FastAPI server entry point
├── requirements.txt      # Python dependencies
├── README.md             # Project overview
├── env_setup.md          # Environment setup guide
└── .gitignore            # Ignore venv, .env, cache files

