# Ambient Email Agent: Comprehensive Project Guide

Welcome to the **Ambient Email Agent**! This guide provides a deep understanding of the project, from its core philosophy to a step-by-step walkthrough for new developers joining the team.

---

## 1. Project Introduction

The **Ambient Email Agent** is an intelligent, automated assistant designed to help users manage their email inbox efficiently. Unlike simple auto-responders, this agent uses **Large Language Models (LLMs)** and **Graph-based Workflows (LangGraph)** to "think" about each email before taking action.

It doesn't just reply blindly; it triages emails, understands context, checks your calendar, and drafts responses that you—the human—can review and approve. It is built to be an "ambient" helper that works in the background but keeps you in the loop for important decisions.

**Built by:** Group A1 (4-member collaborative team)  
**Duration:** 4 Milestones over project timeline  
**Framework:** LangGraph + LangChain + Google Gemini

---

## 2. Team Organization & Responsibilities

This project was developed collaboratively with clear role divisions:

### Aayush Shah - Environment & Infrastructure Lead
- **M1:** Development environment setup, tooling, dependency management
- **M2:** Test dataset creation (100+ examples), ground truth responses
- **M3:** Dangerous tools identification, safety tagging system
- **M4:** Unsafe tool flagging, interrupt configuration, user notifications

[View detailed contributions →](../AayushShah/README.md)

### Ganesh Sai Manideep Bandaru - Triage Node & Dataset Lead
- **M1:** Core ML classification logic, training dataset (48 emails)
- **M2:** Quality metrics definition (Helpfulness, Tone, Accuracy)
- **M3:** HITL checkpoint implementation, state persistence to SQLite
- **M4:** MemorySaver implementation, thread management, dual-layer memory

[View detailed contributions →](../Ganesh_Sai_Manideep_Bandaru/README.md)

### Samruddhi Maslage - ReAct Reasoning Loop & Tooling Lead
- **M1:** ReAct agent brain, mock tools (calendar, contacts)
- **M2:** LLM-as-a-judge evaluator setup in LangSmith
- **M3:** LangSmith tracing, safe/dangerous action test cases
- **M4:** State inspection/update, resume logic, draft modification

[View detailed contributions →](../SamruddhiMaslage/README.md)

### Payal Kokane - HITL + UI & Observability Lead
- **M1:** HITL workflow design, debugging visibility
- **M2:** Batch testing, success rate verification, failure analysis
- **M3:** Pause trigger testing, human input validation
- **M4:** Mock tools, edge case testing, final integration (main4.py)

[View detailed contributions →](../Payal_Kokane/README.md)

---

## 3. Detailed Description & Capabilities

This project implements a sophisticated **Human-in-the-Loop (HITL)** workflow, ensuring AI autonomy never overrides human judgment for critical tasks.

### Core Capabilities:

**Intelligent Triage**  
Automatically categorizes incoming emails into three buckets:
- `ignore`: Newsletters, spam, or low-priority notifications
- `notify-human`: Urgent or important emails requiring your attention
- `respond-act`: Emails where the AI can draft a helpful response

**ReAct Loop (Reasoning + Acting)**  
For `respond-act` emails, the agent enters a reasoning loop:
1. Analyzes the email request
2. Decides if it needs external information (e.g., checking calendar)
3. Executes safe, read-only tools to gather facts
4. Synthesizes information to draft a high-quality reply

**Smart Calendar Integration**
- Detects if an email is asking for a meeting
- Checks your actual availability via Google Calendar
- Drafts replies that offer real, free time slots

**Human-in-the-Loop (HITL)**
- **Nothing is sent automatically** - All drafts presented to you in UI
- You can **Approve**, **Edit**, or **Deny** the AI's proposed draft
- Builds trust and ensures professional communication

**Persistent Memory**
- **Short-term memory:** SQLite checkpointing for crash recovery
- **Long-term memory:** InMemoryStore for preference learning across sessions
- Thread-based conversation tracking

---

## 4. New Developer Onboarding: How to Explore the Project

If you are new to this codebase, follow this path to understand how everything fits together.

### Step 1: Understand the Team Structure
Start by reading the individual contribution docs to see who built what:
- Review [Team Structure & Contributions](#2-team-organization--responsibilities)
- Read individual README files for detailed milestone breakdowns
- Understand the division of labor across 4 milestones

### Step 2: Specific Entry Points (The "Front Door")
Look at how the application interacts with the outside world:

**Backend Entry (`backend/src/main.py`)**  
FastAPI server with API endpoints (`/scan-and-draft`, `/approve-action`). This orchestrates the connection between the web world and the AI brain.

**Frontend Interface (`frontend/app.py`)**  
Streamlit UI handling user login (OAuth) and displaying drafts. Shows how we present AI decisions to humans.

### Step 3: The "Brain" (Workflow Logic)
See how requests are processed:

**The Workflow Graph (`backend/src/graph.py`)**  
Most important file - defines the "flowchart" of the AI. Trace the path: `Start → Triage → Decision → ReAct → HITL → Action`.

**The State (`backend/src/state.py`)**  
Understand what data is passed around. `AgentState` is the "memory" holding email content, message history, and tool outputs.

**Nodes (`backend/src/node.py`)**  
Individual processing units: `triage_node`, `react_model_node`, `action_node`.

### Step 4: The Capabilities (Tools)
Deep dive into what the AI can actually *do*:

**Gmail Tools (`backend/src/tools/google_gmail.py`)**  
How we fetch emails and send replies using Gmail API. Note the safe-guards preventing accidental sends.

**Calendar Tools (`backend/src/tools/google_calendar.py`)**  
Logic for understanding time slots and querying the calendar.

**Mock Tools (`backend/src/tools/tools.py`)**  
Safe development versions for testing without real API calls.

### Step 5: Triage & Classification
Understand the decision-making process:

**Triage Implementation (`triage/triage_node.py`)**  
Hybrid rule-based + ML classification system.

**ML Model (`triage/triage_model/`)**  
Fine-tuned DistilBERT classifier trained on 48-email dataset.

### Step 6: Evaluation & Testing
See how we measure quality:

**LLM-as-a-Judge (`evaluation/judge_evaluation.py`)**  
Custom RunEvaluator for automated quality assessment.

**Test Datasets (`data/`)**  
- `test_emails.csv` - 100+ examples for evaluation
- `golden_set_emails.jsonl` - Reference outputs

**Test Suite (`test/`)**  
Comprehensive pytest suite covering triage, HITL, tools, integration, and edge cases.

### Step 7: Testing & Experimentation
See it in action without breaking anything:

**Notebooks (`notebooks/`)**
- `01_triage_test.ipynb` - Safe playground to test email classification
- `02_react_agent.ipynb` - Watch the "thought process" of the agent

---

## 5. Architecture Overview

### High-Level Workflow

```
Email Received 
  → Triage Classification (ignore/notify/respond-act)
    → If respond-act: ReAct Loop
      → Call Safe Tools (read_calendar, etc.)
      → Generate Draft Reply
      → HITL Checkpoint (Pause)
      → Human Decision (Approve/Edit/Deny)
      → Execute or Cancel Action
```

### Technology Layers

**Presentation Layer**
- Streamlit UI for human interaction
- OAuth2 authentication
- Real-time draft review

**API Layer**
- FastAPI REST endpoints
- Request validation
- Response formatting

**Agent Layer**
- LangGraph workflow orchestration
- LangChain LLM integration
- State management

**Tool Layer**
- Gmail API integration
- Google Calendar API
- Mock implementations for testing

**Data Layer**
- PostgreSQL for persistence
- SQLite for checkpoints
- InMemoryStore for preferences

---

## 6. Key Design Decisions

### Why Hybrid Triage (Rules + ML)?
- **Rules:** Handle obvious cases (promo keywords, system notifications)
- **ML:** Generalize to unseen email patterns
- **Result:** 94.5% accuracy vs 87% with ML alone

### Why Mock Tools?
- **Safety:** No accidental real-world actions during development
- **Speed:** Testing without API rate limits
- **Reliability:** Consistent behavior for automated tests

### Why HITL for Every Draft?
- **Trust:** Users never worry about unauthorized sends
- **Quality:** Human review catches AI mistakes
- **Learning:** Edit feedback improves future drafts

### Why Dual-Layer Memory?
- **Short-term (Checkpoints):** Crash recovery within session
- **Long-term (Store):** Preference learning across sessions
- **Result:** True ambient intelligence that remembers corrections

---

## 7. Quick Setup & Running

### Prerequisites
- Python 3.9+
- PostgreSQL (or SQLite for development)
- Google Cloud Project with APIs enabled

### Installation
```bash
# Clone and install
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your API keys to .env
```

### Run the Application
**1. Start the Brain (Backend)**
```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**2. Start the Face (Frontend)**
```bash
# In a new terminal
streamlit run frontend/app.py --server.port 8501
```

**3. Access the Application**  
Open your browser to `http://localhost:8501` to log in and start processing emails.

---

## 8. Testing Guide

### Run Full Test Suite
```bash
pytest test/ -v
```

### Run Specific Test Categories
```bash
# Triage accuracy
pytest test/test_triage.py -v

# HITL workflow
pytest test/test_hitl.py -v

# Integration tests
pytest test/test_integration.py -v

# Edge cases
pytest test/test_edge_cases.py -v
```

### Manual Testing with Notebooks
```bash
jupyter lab notebooks/
```
- Open `01_triage_test.ipynb` for triage testing
- Open `02_react_agent.ipynb` for ReAct loop inspection

---

## 9. Common Development Tasks

### Adding a New Tool
1. Create tool function in `backend/src/tools/`
2. Tag as safe or dangerous in tool metadata
3. Add mock version for testing
4. Update graph to include tool in available tools
5. Add tests in `test/test_tools.py`

### Modifying Triage Logic
1. Update rules in `triage/triage_node.py`
2. If changing ML: retrain model with `triage/train_model.py`
3. Run evaluation: `pytest test/test_triage.py`
4. Check accuracy doesn't degrade

### Adding New Evaluation Metrics
1. Define metric in `evaluation/metrics.py`
2. Update judge prompt in `evaluation/judge_evaluation.py`
3. Run batch evaluation: `python run_evaluator.py`
4. Review results in LangSmith dashboard

---

## 10. Troubleshooting

### "Import Error" when running backend
- Ensure you're in the correct directory: `cd backend`
- Verify virtual environment is activated
- Run: `pip install -r requirements.txt`

### Gmail API Authentication Fails
- Check `credentials.json` is in `credentials/` folder
- Verify redirect URI in Google Cloud Console: `http://localhost:8000/auth/callback`
- Delete old tokens and re-authenticate

### Agent Gets Stuck in Loop
- Check LangSmith trace for the specific run
- Verify tool descriptions are clear
- Add max iteration limit in graph configuration

### Tests Failing
- Ensure test database is set up: `createdb test_email_db`
- Check environment variables in `.env` vs `.env.test`
- Run with verbose output: `pytest -vv`

---

## 11. Further Reading

- **LangGraph Documentation:** https://langchain-ai.github.io/langgraph/
- **LangSmith Evaluation Guide:** https://docs.smith.langchain.com/
- **Gmail API Reference:** https://developers.google.com/gmail/api
- **Calendar API Reference:** https://developers.google.com/calendar/api

---

## 12. Project Status & Next Steps

**Current Status:** ✅ All 4 Milestones Complete

**Potential Future Enhancements:**
- Real-time email monitoring (webhooks vs polling)
- Multi-user support with separate preferences
- Advanced learning from user corrections
- Mobile app integration
- Slack/Teams integration for notifications

---

**For Questions or Contributions:**  
Contact any team member via their individual documentation or raise an issue in the repository.

---

**Developed by Group A1:**
- Aayush Shah (Environment & Infra Lead)
- Ganesh Sai Manideep Bandaru (Triage & Dataset Lead)
- Samruddhi Maslage (ReAct & Tooling Lead)
- Payal Kokane (HITL & Observability Lead)
