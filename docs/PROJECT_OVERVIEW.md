# Ambient Email Agent: Comprehensive Project Guide

Welcome to the **Ambient Email Agent**! This guide is designed to provide a deep understanding of the project, from its core philosophy to a step-by-step walkthrough for new developers joining the team.

---

## 1. Project Introduction

The **Ambient Email Agent** is an intelligent, automated assistant designed to help users manage their email inbox efficiently. Unlike simple auto-responders, this agent uses **Large Language Models (LLMs)** and **Graph-based Workflows (LangGraph)** to "think" about each email before taking action.

It doesn't just reply blindly; it triages emails, understands context, checks your calendar, and drafts responses that you—the human—can review and approve. It is built to be an "ambient" helper that works in the background but keeps you in the loop for important decisions.

---

## 2. Detailed Description & Capabilities

This project implements a sophisticated **Human-in-the-Loop (HITL)** workflow, ensuring AI autonomy never overrides human judgment for critical tasks.

### Core Capabilities:

*   **Intelligent Triage**: Automatically categorizes incoming emails into three buckets:
    *   `ignore`: Newsletters, spam, or low-priority notifications.
    *   `notify-human`: Urgent or important emails requiring your attention.
    *   `respond-act`: Emails where the AI can draft a helpful response or take action.

*   **ReAct Loop (Reasoning + Acting)**: For `respond-act` emails, the agent enters a reasoning loop:
    *   It analyzes the email request.
    *   It decides if it needs external information (e.g., checking your calendar).
    *   It executes safe, read-only tools (like `read_calendar`) to gather facts.
    *   It synthesizes this information to draft a high-quality reply.

*   **Smart Calendar Integration**:
    *   Detects if an email is asking for a meeting.
    *   Checks your actual availability via Google Calendar.
    *   Drafts replies that offer real, free time slots.

*   **Human-in-the-Loop (HITL)**:
    *   **Nothing is sent automatically.** All drafts are presented to you in a UI.
    *   You can **Approve**, **Edit**, or **Deny** the AI's proposed draft.
    *   This builds trust and ensures professional communication.

---

## 3. New Developer Onboarding: How to Explore the Project

If you are new to this codebase, follow this path to understand how everything fits together.

### Step 1: Specific Entry Points (The "Front Door")
Start by looking at how the application interacts with the outside world.

*   **Backend Entry (`backend/src/main.py`)**: This is the FastAPI server. Look here to see the API endpoints (`/scan-and-draft`, `/approve-action`) that trigger the AI. This file orchestrates the connection between the web world and the AI brain.
*   **Frontend Interface (`frontend/app.py`)**: This is the Streamlit UI. It handles user login (OAuth) and displays the drafts to the user. Scanning this file shows you how we present AI decisions to humans.

### Step 2: The "Brain" (Workflow Logic)
Now that you know how requests come in, see how they are processed.

*   **The Workflow Graph (`backend/src/graph.py`)**: This is the most important file. It defines the "flowchart" of the AI. You'll see nodes like `triage_node`, `react_model`, and `hitl_checkpoint`. Trace the path: `Start -> Triage -> Decision`.
*   **The State (`backend/src/state.py`)**: Understand what data is passed around. `AgentState` is the "memory" of the application, holding the email content, message history, and tool outputs.

### Step 3: The Capabilities (Tools)
Deep dive into what the AI can actually *do*.

*   **Gmail Tools (`backend/src/tools/google_gmail.py`)**: Check how we actually fetch emails and send replies using the Gmail API. Note the safe-guards that prevent accidental sends.
*   **Calendar Tools (`backend/src/tools/google_calendar.py`)**: See the logic for understanding time slots and querying the calendar.

### Step 4: Testing & Experimentation
Finally, see it in action without breaking anything.

*   **Notebooks (`notebooks/`)**:
    *   `01_triage_test.ipynb`: A safe playground to test if the AI correctly classifies emails without running the full server.
    *   `02_react_agent.ipynb`: Watch the "thought process" of the agent as it tries to answer sample emails.

---

## 4. Quick Setup & Running

For detailed dependency installation, refer to `README.md`. Here is the cheatsheet for getting it running daily:

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
