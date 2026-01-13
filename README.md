# Ambient Email Agent using LangGraph - langgraph-email-assistant
"Building an Ambient Agent with LangGraph for an Email Assistant"
<br>
Intelligent ambient agent leveraging LangGraph to process, analyze, and automate email workflows with real-time assistance and proactive insights.

This project implements an **AI-powered ambient email assistant** using **LangGraph**, **LangSmith**, and a **Human-in-the-Loop (HITL)** safety framework.  
The system can read incoming emails, decide what to do, draft replies, pause before taking dangerous actions, and learn from human feedback.

---

## Key Terms Used in This Project

### LangGraph
LangGraph is a framework for building **stateful, multi-step AI agents**.  
Unlike simple LLM calls, LangGraph allows us to define workflows as **graphs** with nodes and edges. Each node performs one step (e.g., triage, reasoning, action), and the state is passed between nodes.

In this project, LangGraph controls:
- Email triage
- ReAct reasoning
- Action execution
- Human-in-the-Loop pauses

---

### StateGraph
A StateGraph is a special LangGraph graph where every step reads and writes to a **shared state object**.  
This allows the agent to remember:
- The email content
- The triage decision
- The drafted reply
- Whether human approval is required

---

### ReAct (Reason + Act)
ReAct is a reasoning pattern where the agent:
1. Thinks about what the email means  
2. Decides what action to take  
3. Produces a draft or performs a tool action  

In our project, the ReAct node generates draft replies and decides whether an action such as sending an email is needed.

---

### Human-in-the-Loop (HITL)
HITL means the AI **must stop and ask a human for permission** before doing something dangerous.

In this project:
- Drafting a reply is safe
- Sending an email or creating calendar events is dangerous
- Dangerous actions cause the agent to pause and wait for:
  - Approve
  - Deny
  - Edit

This prevents the agent from making harmful or irreversible decisions.

---

### LangSmith
LangSmith is a tracing and evaluation platform for LLM systems.  
It records:
- Each agent step
- Each decision
- When the agent pauses
- When it resumes

We use LangSmith to:
- Evaluate response quality
- Verify that HITL pauses trigger correctly
- Visualize agent workflows

---

### LLM-as-a-Judge
Instead of manually grading outputs, we use another LLM to **evaluate the agent’s replies** on:
- Helpfulness
- Tone
- Accuracy

This makes large-scale automated testing possible.

---

##  What We Built (Up to Milestone 3)

### Milestone 1 — Core Agent
We built an email agent that:
- Reads incoming emails
- Classifies them into:
  - Ignore
  - Notify Human
  - Respond
- Generates draft replies using ReAct
- Uses LangGraph to control the workflow

---

### Milestone 2 — Evaluation System
We created:
- A dataset of **100 realistic emails**
- Ground-truth replies for correct behavior
- Quality metrics:
  - Helpfulness
  - Tone
  - Accuracy
- A **LangSmith-based LLM-as-a-Judge** to score replies automatically

This allowed us to identify:
- Classification errors
- Low-accuracy responses
- Where the agent needs improvement

---

### Milestone 3 — Human-in-the-Loop (Safety Layer)
We implemented full **HITL safety**:

1. Dangerous actions were identified:
   - `send_email`
   - `create_calendar_invite`

2. LangGraph was modified with:
   ```python
   interrupt_before=["action_node"]
