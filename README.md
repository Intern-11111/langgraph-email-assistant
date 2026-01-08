---

# LangGraph Email Assistant

A smart email triage and automation system powered by **LangGraph**, **LangChain**, **FastAPI**, and **Hugging Face Transformers**.

---

## Milestone 1 — Core System Setup & Basic Email Triage Agent

### Goal of Milestone 1

Establish the foundation required for building a fully autonomous email assistant:

* Setup Python environment & architecture
* Validate AI framework compatibility
* Build basic triage logic for email routing
* Enable experimental evaluation via APIs

---

## Key Contributions

###  1️⃣ Environment & Infrastructure (Developer: Lead Responsibility)

The development environment was fully prepared including:

* Virtual environment configuration (`venv`)
* Installation of all key dependencies
* `.gitignore` rules to exclude:

  * `venv/`, `.env`, cache folders, temporary artifacts
* Modular project structure designed for future scalable growth

**Verified Libraries**

| Library      | Purpose                         |
| ------------ | ------------------------------- |
| langchain    | Prompt orchestration            |
| langgraph    | State machine for agent control |
| transformers | LLM model execution (TinyLlama) |
| fastapi      | Backend API                     |
| uvicorn      | Server for local testing        |
| datasets     | Loading evaluation dataset      |

---

### 2️⃣ Email Triage Agent

The first version of the intelligent agent uses logical heuristics to classify incoming emails into three triage categories:

| Category         | Meaning                          | Action                |
| ---------------- | -------------------------------- | --------------------- |
| **ignore**       | Spam, marketing, irrelevant      | Drop silently         |
| **notify_human** | Ambiguous, risky, legal concerns | Alert a human         |
| **respond**      | Routine business queries         | Auto-reply generation |

#### Agent Flow

```
Incoming Email 
        ↓
   TRIAGE NODE (decision logic)
        ↓
 Respond? ——— Yes → React Node (draft reply)
        ↓
  Final Output → response + reasoning
```

Components Built:

* **Triage Node**

  * Keyword pattern heuristics
  * Risk scoring
* **ReAct Draft Reply Node**

  * Generates polite short email replies using LLM

---

###  3️⃣ Evaluation & Demo

✔ Integrated dataset:
`SetFit/enron_spam` from Hugging Face

✔ Full evaluation tooling added:

* Accuracy measurement
* Ground-truth comparison for triage decisions
* Logging reason behind predictions

✔ FastAPI endpoints implemented:

| Endpoint | Description                  |
| -------- | ---------------------------- |
| `/eval`  | Run evaluation benchmark     |
| `/run`   | Test with custom input email |

Example output:

```json
{
  "triage_decision": "respond",
  "draft_reply": "Sure, happy to assist! Can you clarify…?",
  "reason": "Heuristic analysis of business coordination intent"
}
```

---

##  Project Structure

```
langgraph-email-assistant/
│
├── src/
│   ├── api/             # FastAPI routes + LLM provider
│   ├── graph/           # LangGraph build + agent state
│   ├── triage/          # Email triage logic
│   ├── agents/          # ReAct agent behavior
│   ├── utils/           # Support helpers
│
├── data/                # Datasets + test corpora
├── results/             # Outputs generated from evaluation
│
├── run_server.py        # Local API entry point
├── requirements.txt     # Dependencies list
├── README.md            # Project documentation
├── env_setup.md         # Setup instructions
└── .gitignore           # Ignore unnecessary files
```

---

##  Status of Milestone 1

| Feature                  | Status        |
| ------------------------ | ------------- |
| Env setup                |   Done        |
| Model integration        |   Done        |
| LangGraph pipeline       |   Done        |
| Heuristic triage         |   Done        |
| Evaluation + API         |   Done        |
| Ready for next milestone |   Approved    |

---
---

#  **Milestone 2 – Agent Evaluation & Quality Metrics**

##  Objective

Evaluate the LangGraph-based Email Triage Agent using structured datasets and measure accuracy, decision quality, and behavior across key email categories:

* **Respond** (coordination, confirmations)
* **Notify Human** (legal, financial, escalation)
* **Ignore** (spam, ads, phishing)

---

##  **Dataset Overview**

We constructed the evaluation dataset in **3 batches** aligned with triage decisions:

| Batch       | Dataset File                     | Category     | Count | Description                                  |
| ----------- | -------------------------------- | ------------ | ----: | -------------------------------------------- |
| **Batch 1** | `m2_testset_batch1_respond.json` | Respond      |   ~40 | Valid normal communication requiring a reply |
| **Batch 2** | `m2_testset_batch2_notify.json`  | Notify Human |   ~40 | Risk-sensitive content requiring escalation  |
| **Batch 3** | `m2_testset_batch3_ignore.json`  | Ignore       |   ~40 | Spam, marketing, phishing, irrelevant        |

 Total dataset size evaluated: **121 emails**

---

##  Evaluation Implemented

The endpoint:

```
GET /eval/evaluate
```

✔ Runs graph on entire dataset
✔ Computes classification correctness
✔ Scores reply quality for respond-case emails
✔ Writes results to:

 `/results/m2_eval_report.json`

---

##  Metrics Measured

| Metric                        | Purpose                               | Scale |
| ----------------------------- | ------------------------------------- | ----- |
| **Accuracy**                  | Correct triage decisions              | 0–1   |
| **Triage Score**              | Direct match to ideal label           | 0–1   |
| **Reply Quality Score**       | Relevance, keyword overlap            | 0–1   |
| **Tone Score**                | Courtesy markers (please/thanks etc.) | 0–1   |
| **Format Score**              | Decision validity                     | 0–1   |
| **Latency Score**             | Response speed                        | 0–1   |
| **Hallucination Score**       | Staying inside context                | 0–1   |
| **Agent Quality Score (AQS)** | Weighted overall quality              | 0–1   |

**AQS = Weighted combination of above dimensions**

---

## Milestone-2 Results (Summary)

| Metric                                |    Result |
| ------------------------------------- | --------: |
| **Total Emails Evaluated**            |       121 |
| **Correct Predictions**               |        54 |
| **Overall Accuracy**                  | **44.6%** |
| **Average Agent Quality Score (AQS)** |  **0.43** |

---

## Observations

✔ **Notify Human** and **Ignore** detection using heuristics works well
✔ Spam / risky content classification is reliable
✔ Respond-case emails lack strong reasoning → Many false escalations

⚠ **Latency extremely high** (CPU inference with 1.1B model)
⚠ Misclassification for short casual requests ("Can we talk?")
⚠ Reply generation too generic (low overlap score)

---
<br>

## Milestone 2 – Agent Upgrade + Tuning

### Major Improvements

| Feature                                                        | Status |
| -------------------------------------------------------------- | ------ |
| Switched from TinyLlama → **DeepSeek-R1 (via OpenRouter API)** | ✅      |
| Real LLM-based reply generation                                | ✅      |
| JSON-schema response enforcement                               | ✅      |
| Better reasoning prompts                                       | ✅      |
| Expanded agent evaluation framework                            | ✅      |

The updated **ReAct reasoning node** ensures:

* Polite + context-aware replies
* No hallucination beyond given email
* JSON-only formatted outbound response

###  Accuracy Boost  to   84%

After model upgrade + tuning:

| Metric                 | Before    | After   |
| ---------------------- | --------- | ------- |
| Overall Accuracy       | **44.6%** | **84%** |
| Respond accuracy       | Medium    | High    |
| Notify-human precision | High      | High    |
| Spam filtering         | High      | High    |

| Metric                                |    Result |
| ------------------------------------- | --------: |
| **Total Emails Evaluated**            |       121 |
| **Correct Predictions**               |       100 |
| **Overall Accuracy**                  | **84.6%** |
| **Average Agent Quality Score (AQS)** |  **0.83** |

Signed-off evaluation stored at:

```
results/m2_eval_report.json
```
---

## ▶ Running Locally

```bash
git clone https://github.com/Intern-11111/langgraph-email-assistant.git
cd langgraph-email-assistant
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn run_server:app --reload
```

Open in browser:

```
http://localhost:8000/docs
```

Evaluate the model:

```
GET /eval/evaluate
```

## Deliverables Completed in M2

| Feature                               | Status |
| ------------------------------------- | :----: |
| Graph agent integrated with evaluator |    ✅   |
| Test dataset ingestion                |    ✅   |
| Scoring system implementation         |    ✅   |
| JSON evaluation export                |    ✅   |
| Performance analysis                  |    ✅   |

---

## Files Added in Milestone-2

```
src/eval/evaluator.py
src/api/eval_router.py
data/m2_testset_batch1_respond.json
data/m2_testset_batch2_notify.json
data/m2_testset_batch3_ignore.json
results/m2_eval_report.json (auto-generated)
```
---

# Milestone 3 – Human-in-the-Loop (HITL) Safety & Checkpointing

## LangGraph Email Assistant

---

## Objective of Milestone 3

Milestone 3 focuses on **agent safety, control, and recoverability**.

The goal is to ensure that the email assistant:

* Can reason autonomously
* **Never performs irreversible actions without human approval**
* Can **pause safely** before such actions
* Can **resume execution without losing memory**

This milestone implements all **Intern-1 safety requirements** using **LangGraph checkpoints and Human-in-the-Loop (HITL) controls**.

---

Here’s the **clean, correctly formatted version** you can paste directly into your README (the `/n` was just line-break text leaking through):

---

## Key Features Implemented

* ✔ **Dangerous tool identification**
* ✔ **Undo Test enforcement**
* ✔ **Human-in-the-Loop (HITL) checkpoint**
* ✔ **Safe pause before irreversible actions**
* ✔ **State preservation (“Saving the Game”)**
* ✔ **Controlled resume after human decision**
---

## Core Concept: Undo Test

> **Undo Test Rule**
> If an action changes reality and cannot be undone, it is considered **dangerous**.

### Examples

| Action                | Undoable? | Classification |
| --------------------- | --------- | -------------- |
| Read email            | ✅ Yes     | Safe           |
| Classify email        | ✅ Yes     | Safe           |
| Draft reply           | ✅ Yes     | Safe           |
| Send email            | ❌ No      | Dangerous      |
| Create calendar event | ❌ No      | Dangerous      |
| Delete data           | ❌ No      | Dangerous      |

Only **dangerous actions** require human approval.

---

## Dangerous Tool Identification

Dangerous tools are explicitly defined in the system.

**File:** `src/config/tools.py`

```python
DANGEROUS_TOOLS = {
    "send_email",
    "create_calendar_invite",
    "spend_money",
    "delete_file",
    "update_database",
}

def is_dangerous_tool(tool_name: str) -> bool:
    return tool_name in DANGEROUS_TOOLS
```

This ensures:

* The LLM cannot bypass safety rules
* All irreversible actions are centrally controlled

---

## Agent Planning vs Execution (Critical Design)

The agent **never executes actions directly**.

Instead, it:

1. **Plans** an action
2. **Tags** it as dangerous if applicable
3. **Pauses** execution
4. **Waits** for human approval
5. **Executes** only after approval

---

## ReAct Node – Planning & HITL Trigger

**File:** `src/agents/react_loop.py`

Key responsibilities:

* Generate a draft reply
* Plan the intended action
* Tag dangerous tools
* Trigger HITL pause

```python
state.selected_tool = "send_email"
state.tool_payload = {"body": state.draft_reply}

if is_dangerous_tool(state.selected_tool):
    state.hitl_required = True
```

**Important safeguard**
The LLM is executed **only once**. After HITL approval, the agent **does not re-run reasoning**.

---

## Human-in-the-Loop (HITL) Checkpoint

The LangGraph is compiled with an interruption **before the action node**.

**File:** `src/graph/email_graph.py`

```python
return graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["action_node"]
)
```

This guarantees:

* No irreversible action runs automatically
* Human approval is mandatory

---

## Saving the Game (Checkpointing)

Milestone 3 uses **in-memory checkpointing** to demonstrate correct pause–resume behavior.

**File:** `src/graph/checkpoint.py`

```python
from langgraph.checkpoint import MemorySaver

checkpointer = MemorySaver()
```

### What is saved?

* Drafted reply
* Agent reasoning
* Tool choice
* HITL flag
* Execution position

The agent can pause **without forgetting anything**.

> Persistence across restarts is intentionally deferred to Milestone 4.

---

## Action Node – Controlled Execution

**File:** `src/graph/email_graph.py`

The action node is the **only place** where real-world effects occur.

```python
def action_node(state: EmailState) -> EmailState:
    if state.human_decision == "deny":
        print("ACTION DENIED — no email sent")

    elif state.human_decision == "edit":
        print("EMAIL SENT (EDITED)")
        print(state.edited_reply)

    elif state.human_decision == "approve":
        print("EMAIL SENT (APPROVED)")
        print(state.draft_reply)

    return state
```

This ensures:

* Deny → nothing happens
* Edit → edited reply is sent
* Approve → auto-drafted reply is sent

---

## HITL API Flow

### Process Email

**Endpoint**

```
POST /triage/email
```

If a dangerous action is planned:

* Graph pauses
* Thread ID is returned
* State is checkpointed

---

### Human Decision

**Endpoint**

```
POST /triage/hitl/decision
```

Parameters:

* `thread_id`
* `decision` → approve | deny | edit
* `edited_reply` (required for edit)

The graph resumes safely from the checkpoint.

---

## Demonstration Scenarios

### 🟢Safe Case (No HITL)

* Newsletter
* Informational email
* Draft-only response

Result:

* No pause
* No human intervention

---

### 🔴 Dangerous Case (HITL Triggered)

* Meeting confirmation
* Email reply that would be sent

Result:

```
LLM GENERATED DRAFT
HITL PAUSED, awaiting human decision...
THREAD_ID: xxxx
```

After approval:

```
EMAIL SENT (APPROVED)
```

---

## Task Completion Checklist

| Requirement              | Status |
| ------------------------ | ------ |
| Identify dangerous tools | ✅      |
| Apply Undo Test          | ✅      |
| Tag dangerous actions    | ✅      |
| Add HITL checkpoint      | ✅      |
| Save agent state         | ✅      |
| Pause without forgetting | ✅      |
| Use interrupt_before     | ✅      |

---
## Key Takeaway

> **The agent can think autonomously but acts only with human consent.
> Safety, control, and recoverability are guaranteed by design.**

---
## Files Added / Updated (Milestone 3)

| File                       | Type    | Purpose                                                            |
| -------------------------- | ------- | ------------------------------------------------------------------ |
| `src/agents/react_loop.py` | Updated | Drafts replies, plans actions, tags dangerous tools, triggers HITL |
| `src/graph/email_graph.py` | Updated | Adds `action_node` and HITL interruption before execution          |
| `src/graph/state.py`       | Updated | Adds HITL fields and action planning metadata                      |
| `src/api/hitl_router.py`   | Added   | API endpoint for approve / deny / edit decisions                   |
| `src/hitl/helpers.py`      | Added   | Handles graph pause–resume logic                                   |
| `src/config/tools.py`      | Added   | Central registry for dangerous vs safe tools (Undo Test)           |
| `src/graph/checkpoint.py`  | Added   | Configures LangGraph checkpointing (MemorySaver)                   |

---

**Milestone 3 is complete, functional, and demonstrable.**

---
