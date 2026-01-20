

# Ambient Email Agent (Triage + ReAct + Evaluation)

This project is an email assistant built with **LangGraph**, **LLMs** (Gemini / Hugging Face), and **LangSmith**.  
It can:

- Classify incoming emails into:
  - `ignore`
  - `notify-human`
  - `respond-act`
- For `respond-act`, run a small **ReAct loop**:
  - Decide whether to call safe mock tools (like `read_calendar`)
  - Draft a reply using the tool results

Milestone 2 adds an automated **LLM-as-a-judge** evaluation framework in LangSmith that scores the quality of the agent’s replies (helpfulness, tone, instruction-following).[web:195][web:174]

Milestone 3: Human-in-the-Loop (HITL) safety - pauses for dangerous actions (send_email)

Milestone 4: Persistent Memory + Live Gmail/Calendar API integration

---

## 1. Project structure



## 1. Project Structure

<img width="723" height="803" alt="image" src="https://github.com/user-attachments/assets/92cb68f0-0c83-44a8-9f89-c7b21e48c312" />


---

## 2. LLM + LangSmith config (`config.py`)

- Configures chat models:
  - `gemini_ai_model()` → Google Gemini chat model.
  - `hugging_face_model()` → optional Hugging Face chat model.
- Loads API keys from `.env` (Gemini, Hugging Face, LangSmith).  
- With `LANGCHAIN_TRACING_V2=true` and `LANGCHAIN_API_KEY` set, all LangGraph runs are traced into LangSmith for debugging and evaluation.[web:195][web:188]

---

## 3. State definition (`state.py`)

Shared state that flows through the graph:


class AgentState(TypedDict):
messages: list[BaseMessage] # conversation history
mail: dict # {"subject": str, "body": str}
triage_category: Literal["ignore", "notify-human", "respond-act"]
tool_name: str | None # name of tool to call (inside ReAct)
tool_args: dict | None # arguments for that tool
final_reply: str | None # drafted reply for respond-act emails
hitl: Optional[Dict[str, Any]]   # {"tool": str, "args": dict, "proposed_reply": str | None, ...}
hitl_decision: Optional[Literal["pending", "approve", "deny", "edit"]]

- `messages` – chat history the ReAct loop reasons over.  
- `mail` – current email being processed.  
- `triage_category` – output of the triage step.  
- `tool_name` / `tool_args` – used only when a tool is called.  
- `final_reply` – final drafted reply for `respond-act` emails.
- `hitl_decision` - human's response to the pending HITL action.

---

## 4. Triage node and ReAct loop nodes (`node.py` – `triage_node` -  `react_model_node` - `react_tools_node`)
This system uses a Triage-ReAct architecture to process emails, ensuring high-risk actions are reviewed by a human before execution.

State Management: Tracks email history, categorization, and a Human-in-the-Loop (HITL) status to pause for approvals.
Triage Node: A Gemini-powered classifier that decides whether to ignore an email, notify a human, or trigger a task (86% accuracy).
Safety Guardrails: All "dangerous" actions—like sending a reply or booking a calendar event—are automatically blocked until a human selects approve or edit.
Memory & Live Integration: Uses SQLite to remember user preferences across sessions and connects to live Gmail/Calendar APIs via Docker.


| From Node       | Triage Category | Tool Called      | HITL Status | Next Node           |
| --------------- | --------------- | ---------------- | ----------- | ------------------- |
| triage_node     | ignore          | None             | None        | ignore → END        |
| triage_node     | notify-human    | None             | None        | notify_human → END  |
| react_model     | respond-act     | read_calendar    | Safe        | react_tools         |
| react_model     | respond-act     | send_gmail_reply | pending     | hitl_checkpoint     |
| hitl_checkpoint | respond-act     | send_gmail_reply | approve     | Tool executes → END |

---
## 6. Graph flow (`graph.py`) and `run_email_agent()`

The system uses a StateGraph to orchestrate the email lifecycle through four key milestones:

Triage & Routing: Filters mail into three paths. ignore and notify-human terminate immediately, while respond-act initiates the ReAct subgraph.
ReAct Logic: A loop where the model reasons (react_model) and executes tasks (react_tools) such as checking calendars or drafting replies.
HITL Safety: A mandatory hitl_checkpoint that pauses the graph whenever a "dangerous" tool (e.g., send_gmail_reply) is called, requiring human approval to resume.
Persistent Memory: Integrated SQLite MemorySaver that checkpoints the state at every node, enabling cross-session learning and the ability to resume paused tasks.

<img width="407" height="244" alt="image" src="https://github.com/user-attachments/assets/ecc13e52-e1bc-4a06-8e8e-88662c08937b" />


---

## 7. Evaluation framework (Milestone 2)

###  7.1 Golden evaluation dataset

- File: `data/golden_set_emails.jsonl`  
- Contains 100+ realistic emails with:
  - `id`
  - `subject`
  - `body`
  - `triage_label` (expected triage category)
  - `ideal_response` (short description of the perfect reply / outcome)
- Uploaded to LangSmith as a Dataset (e.g. `Golden_DataSet`), mapping:
  - Inputs: `subject`, `body`
  - References: `ideal_response`, `triage_label`.[web:195]

###  7.2 LLM‑as‑a‑judge evaluator in LangSmith

Custom evaluator (e.g. `email_judge`) whose prompt tells the judge to read:

- Original email (subject + body)  
- Ideal outcome (`ideal_response`)  
- Assistant reply (`model_output`)

The judge returns three numeric scores (1–5):

- **helpfulness** – does the reply address the main request and move the task forward?  
- **tone** – is the tone polite and professionally appropriate?  
- **instruction_following** – how well does it match the ideal outcome (dates, confirmations, actions)?[web:174]

These three criteria are configured in the UI as 1–5 score fields.

###  7.3 Evaluation runner (`src/eval_runner.py`)

Connects dataset, agent, and judge:

from langsmith import Client
from langsmith.evaluation import evaluate
from graph import run_email_agent

client = Client()

def eval_wrapper(example):
subject = example.inputs["subject"]
body = example.inputs["body"]
result = run_email_agent(subject=subject, body=body)
return {
"model_output": result["reply"], # graded by email_judge
"triage_prediction": result["triage"] # optional extra field
}

results = evaluate(
eval_wrapper,
data="Golden_DataSet", # LangSmith dataset name
evaluators=["email_judge"], # LLM-as-a-judge evaluator
experiment_prefix="milestone-2",
)


Running this script:

- Executes the agent on all 100+ emails.  
- Calls the judge on each output.  
- Logs an experiment in LangSmith with per‑example and aggregate scores.[web:198][web:268]

You can inspect:

- Average `helpfulness` / `tone` / `instruction_following` per experiment.  
- Individual traces for low‑scoring cases.

This fulfills Milestone 2’s requirement for a fully automated evaluation framework.[web:188]

---

## 8. Notebooks

###  8.1 Triage Accuracy `01_triage_evaluation.ipynb`

This notebook evaluates the Milestone 1 classifier. It runs a test dataset through the graph and generates an accuracy score and a confusion matrix to visualize how well the agent distinguishes between ignore, notify-human, and respond-act.

### 8.2 Agent Reasoning `02_react_agent.ipynb`

Used to inspect the ReAct loop logic. It processes complex emails that require tool usage (like calendar checks) and prints the step-by-step reasoning process alongside the final drafted reply.

###  8.3 LangSmith Evaluation `03_evaluation.ipynb`

The interface for Milestone 2. It connects to the Golden Dataset and triggers automated "LLM-as-a-judge" scoring, providing metrics on helpfulness, tone, and instruction following.


###  8.4 HITL Demonstration (04_hitl_demo.ipynb)

A complete demonstration of Milestone 3 & 4. It shows the graph pausing for human approval on dangerous actions, handling manual edits to drafts, and utilizing persistent memory to resume sessions.

## 9. How to run

###  9.1 Install and set up

pip install -r requirements.txt

Create `.env`:

- GOOGLE_API_KEY=your_gemini_key
- LANGCHAIN_API_KEY=your_langsmith_key
- LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
- LANGCHAIN_TRACING_V2=true
- LANGCHAIN_PROJECT=ambient-email-agent

### 9.3 Automated Evaluation
python -m src.eval_runner

### 9.2 Module Testing


- python tests/test_gamil.py
- python tests/test_calendar.py
- python tests/test_hitl.py
