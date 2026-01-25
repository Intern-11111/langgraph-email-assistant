# Ambient Email Agent - Group A1

**Project**: Building an Ambient Agent with LangGraph for an Email Assistant  
**Team**: Group A1 - 4 Members  
**Framework**: LangGraph + LangChain + Google Gemini  
**Focus**: Intelligent Email Triage, ReAct Reasoning, HITL Workflow, Persistent Memory

---

## Overview

The **Ambient Email Agent** is an intelligent automated assistant that uses Large Language Models (LLMs) and Graph-based Workflows (LangGraph) to manage email inboxes efficiently. The agent doesn't just reply automatically—it triages emails, understands context, checks calendars, and drafts responses that humans can review and approve through a comprehensive Human-in-the-Loop (HITL) workflow.

---

## Team Structure & Contributions

Our team of 4 members worked collaboratively across 4 milestones, with each member taking leadership in specific areas:

| Member | Role | Primary Focus |
|--------|------|---------------|
| **Aayush Shah** | Environment & Infra Lead | Development setup, tooling, test datasets, safety mechanisms |
| **Ganesh Sai Manideep Bandaru** | Triage Node & Dataset Lead | ML classification, quality metrics, memory persistence |
| **Samruddhi Maslage** | ReAct Reasoning Loop & Tooling Lead | Agent brain, mock tools, LLM-as-a-judge evaluations |
| **Payal Kokane** | HITL + UI & Observability Lead | Human safety controls, testing, final integration |

For detailed individual contributions, see:
- [Aayush Shah's README](../AayushShah/README.md)
- [Ganesh Sai Manideep Bandaru's README](../Ganesh_Sai_Manideep_Bandaru/README.md)
- [Samruddhi Maslage's README](../SamruddhiMaslage/README.md)
- [Payal Kokane's README](../Payal_Kokane/README.md)

---

## Project Milestones

### Milestone 1: Basic Agent & Triage
**Goal:** Build foundational email classification and agent workflow

**Team Contributions:**
- **Aayush:** Environment setup, dependency management, project structure
- **Ganesh:** Core ML logic for triage (3-class classifier), golden dataset (48 emails)
- **Samruddhi:** ReAct reasoning loop, mock tools (calendar, contacts)
- **Payal:** HITL workflow design, debugging visibility, initial dashboard

**Deliverables:**
- ✅ Triage node with 3 categories (ignore, notify-human, respond-act)
- ✅ Rule-based + ML hybrid classification
- ✅ ReAct loop for respond-act emails
- ✅ Safe mock tools for development

---

### Milestone 2: Evaluation Framework (LLM-as-a-Judge)
**Goal:** Measure agent quality using structured evaluation pipeline

**Team Contributions:**
- **Aayush:** 100+ email test dataset creation, ground truth responses, CSV/JSON formatting
- **Ganesh:** Quality metrics definition (Helpfulness, Tone, Accuracy), scoring rubric (1-5 scale)
- **Samruddhi:** LLM-as-a-judge evaluator in LangSmith, custom evaluators, automatic scoring
- **Payal:** Batch testing runner, success rate verification, failure analysis

**Deliverables:**
- ✅ 100+ email golden evaluation dataset
- ✅ Custom quality metrics with structured scoring
- ✅ LangSmith integration for automated evaluation
- ✅ Comprehensive failure analysis and root cause diagnosis

---

### Milestone 3: Human-in-the-Loop (HITL) Implementation
**Goal:** Add safety controls to prevent unauthorized dangerous actions

**Team Contributions:**
- **Aayush:** Dangerous tools identification, tool safety tagging, undo test framework
- **Ganesh:** HITL checkpoint in graph, state persistence to SQLite, interrupt_before implementation
- **Samruddhi:** LangSmith tracing connection, test cases for safe/dangerous actions
- **Payal:** Pause trigger testing, human input validation, comprehensive test suite

**Deliverables:**
- ✅ Complete HITL workflow with Approve/Edit/Deny controls
- ✅ Agent pauses before dangerous actions (100% accuracy)
- ✅ State persistence to database (checkpoints.sqlite)
- ✅ LangSmith tracing for full observability

---

### Milestone 4: Persistent Memory & Final Assembly
**Goal:** Enable learning across sessions and deliver integrated system

**Team Contributions:**
- **Aayush:** Unsafe tool flagging, interrupt configuration, user notification system
- **Ganesh:** MemorySaver implementation, Thread ID management, dual-layer memory architecture
- **Samruddhi:** State inspection/update, resume logic, draft modification demonstration
- **Payal:** Mock tools creation, edge case testing, final script assembly (main4.py)

**Deliverables:**
- ✅ Dual-layer memory (short-term checkpointing + long-term store)
- ✅ Thread-based session management
- ✅ Resume logic after human intervention
- ✅ Comprehensive edge case testing (50+ test cases)
- ✅ Final integrated application with complete test suite

---

## Core Features

### Intelligent Email Triage
- Automatically categorizes emails into ignore, notify-human, or respond-act
- Hybrid approach: rule-based preprocessing + ML classification
- 94.5% accuracy on test dataset

### ReAct Reasoning Loop
- Reason → Act → Observe cycle for complex email handling
- Safe tool execution (read_calendar, get_user_prefs, lookup_contact)
- Dangerous action detection and HITL pause

### Human-in-the-Loop Safety
- **100% prevention** of unauthorized dangerous actions
- User approval required for: email sending, calendar modifications, data changes
- Approve/Edit/Deny controls with state modification support

### Persistent Memory
- **Short-term:** SQLite checkpointing for crash recovery
- **Long-term:** InMemoryStore for preference learning across sessions
- Thread-based conversation tracking

### Gmail & Calendar Integration
- Fetch unread emails via Gmail API
- Check availability via Google Calendar API
- Smart meeting detection and response generation
- OAuth2 secure authentication

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **LLM Framework** | LangChain + LangGraph |
| **AI Models** | Google Gemini 2.5 Flash |
| **ML Framework** | Hugging Face Transformers (distilbert) |
| **Backend API** | FastAPI |
| **Frontend UI** | Streamlit |
| **Database** | PostgreSQL + AsyncPostgresSaver |
| **Persistence** | SQLite (checkpoints) + InMemoryStore |
| **Email/Calendar** | Gmail API, Google Calendar API |
| **Authentication** | OAuth2 (Google) |
| **Evaluation** | LangSmith + LLM-as-a-Judge |
| **Testing** | pytest + custom test harness |

---

## Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL (for production) or SQLite (for development)
- Google Cloud Project with Gmail/Calendar APIs enabled

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your API keys to .env
```

### Environment Variables
```env
# LLM API Keys
GOOGLE_API_KEY=your_gemini_api_key
HUGGINGFACEHUB_API_TOKEN=your_hf_token  # optional

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/email_assistance_db

# LangSmith (Optional - for monitoring)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=ambient-email-agent
```

### Run the Application
```bash
# Terminal 1: Backend
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
streamlit run frontend/app.py --server.port 8501
```

Visit `http://localhost:8501` and log in with Google OAuth.

---

## Testing

### Run Full Test Suite
```bash
pytest test/ -v
```

### Available Test Categories
- **Triage Tests** (`test_triage.py`) - Classification accuracy
- **Agent Tests** (`test_hitl.py`) - HITL workflow validation
- **Tool Tests** (`test_calendar.py`, `test_gmail.py`) - API integration
- **Edge Case Tests** (`test_edge_cases.py`) - Rejection, interruption handling
- **Integration Tests** (`test_integration.py`) - End-to-end workflow

### Test Results Summary
- **Triage Accuracy:** 94.5%
- **HITL Pause Trigger:** 100% (no false positives)
- **Draft Quality:** 89.2% acceptable or better
- **Safety Compliance:** 100% (no unauthorized actions)
- **Edge Cases Covered:** 50+ scenarios

---

## Project Structure

```
project_root/
├── backend/src/
│   ├── main.py                 # FastAPI application
│   ├── graph.py                # LangGraph workflow
│   ├── state.py                # AgentState definition
│   ├── node.py                 # Triage, ReAct, Action nodes
│   ├── tools/
│   │   ├── google_gmail.py     # Gmail integration
│   │   ├── google_calendar.py  # Calendar integration
│   │   └── tools.py            # Mock tools
│   └── HITL/
│       ├── hitl_graph.py       # HITL workflow
│       └── execute_tool.py     # Safe tool execution
│
├── frontend/
│   └── app.py                  # Streamlit UI
│
├── triage/
│   ├── triage_node.py          # Triage implementation
│   ├── triage_model/           # Trained classifier
│   └── emails_triage.json      # Training dataset
│
├── evaluation/
│   ├── judge_evaluation.py     # LLM-as-a-judge
│   ├── metrics.py              # Quality metrics
│   └── test_*.py               # Test suites
│
├── data/
│   ├── test_emails.csv         # 100+ test dataset
│   └── golden_set_emails.jsonl # Evaluation dataset
│
├── test/
│   └── (comprehensive test suite)
│
└── docs/
    ├── FINAL_REPORT.md
    └── (individual member documentation)
```

---

## Workflow Diagram

```mermaid
graph TD
    A[Email Received] --> B[Triage Classification]
    B --> C{Category?}
    C -->|ignore| D[Mark as Read]
    C -->|notify-human| E[Label as AI-Notify]
    C -->|respond-act| F[ReAct Reasoning Loop]
    F --> G[Call Safe Tools]
    G --> H[Generate Draft Reply]
    H --> I[HITL Checkpoint - Pause]
    I --> J{Human Decision}
    J -->|Approve| K[Send Original Draft]
    J -->|Edit| L[Update State → Send Edited Draft]
    J -->|Deny| M[Mark as Read Only]
```

---

## Key Achievements

1. **Robust Triage System** - 94.5% accuracy with hybrid rule + ML approach
2. **Safe Development** - Mock tools prevent accidental real-world actions
3. **100% Safety Compliance** - No dangerous actions without human approval
4. **Comprehensive Evaluation** - LLM-as-a-judge with 100+ test cases
5. **Production-Ready HITL** - Pause, review, modify, resume workflow
6. **Persistent Memory** - Dual-layer architecture for crash recovery and learning
7. **Complete Integration** - Backend API + Frontend UI + Database + External APIs

---

## Documentation

- **[FINAL_REPORT.md](FINAL_REPORT.md)** - Complete project summary
- **[PROJECT_GUIDE.md](PROJECT_GUIDE.md)** - New developer onboarding guide
- **Individual Contributions:**
  - [Aayush Shah](../AayushShah/README.md)
  - [Ganesh Bandaru](../Ganesh_Sai_Manideep_Bandaru/README.md)
  - [Samruddhi Maslage](../SamruddhiMaslage/README.md)
  - [Payal Kokane](../Payal_Kokane/README.md)

---

## Acknowledgments

- **LangChain & LangGraph** - For the agent framework
- **Google Gemini** - For LLM capabilities
- **Hugging Face** - For transformer models
- **FastAPI & Streamlit** - For web frameworks
- **Gmail & Calendar APIs** - For email/calendar integration
- **Infosys Springboard** - For the internship opportunity

---

**Status:** ✅ Complete - All 4 Milestones Delivered  
**Team:** Group A1 (4 Members)  
**Project Repository:** [langgraph-email-assistant](https://github.com/your-repo)
