
# Building an Ambient Agent with LangGraph for an Email Assistant

## 1 Project Objective

The primary objective of this project is to design, build, and deploy a next-generation autonomous email assistant using LangGraph.

This project goes beyond a simple reactive agent. Instead, it focuses on creating a sophisticated “ambient” agent that can proactively manage email workflows by combining:

Stateful memory

Human-in-the-Loop (HITL) architecture

Robust evaluation and observability using LangSmith

## 2 Project Workflow

The email assistant follows a structured, state-driven workflow:

### 1. Email Ingestion

A new email is received (e.g., via Gmail API).

### 2. Load Memory

The agent retrieves stored user preferences, past feedback, and context.

### 3. Triage (Decision Stage)

The agent classifies the email into one of three categories:

ignore

Email is archived.

Workflow ends.

notify_human

Email is flagged for user review.

Workflow ends.

respond / act

Triggers the main reasoning loop.

### 4. ReAct Loop (Reason + Act)

Once in the reasoning phase, the agent follows the ReAct pattern:

Reason

The LLM decides the next step
(e.g., “I need to check the calendar”)

Act

The LLM selects and executes an appropriate tool
(e.g., read_calendar)

### 5. Human-in-the-Loop (HITL) Checkpoint

Before executing sensitive actions:

Safe tools

Execute automatically
(e.g., reading calendar, fetching data)

Dangerous tools

Pause execution and wait for human approval
(e.g., sending emails, modifying data)

👤 6. Human Review (Ambient Interaction)

The human reviewer can:

Approve

Agent executes the action and continues.

Deny

Agent stops execution.

Workflow ends.

Edit

Agent updates its memory with corrections.

Executes the revised action.

### 7. Completion

The ReAct loop continues until the task is completed.

Workflow ends successfully.

## 3. Project Directory Structure

A typical project directory structure for this application is shown below:

```text
project_root/
│
├── src/
│   ├── agent/
│   │   ├── react_node.py
│   │   └── tool_call.py
│   │
│   ├── triage/
│   │   ├── triage_node.py
│   │   ├── triage_rules.py
│   │   └── triage_llm.py
│   │
│   ├── data/
│   │   └── emails.json
|   |   ├── golden_set_emails.jsonl
│   │
│   ├── tools/
│   │   ├── calendar.py
│   │   └── contact.py
│   │
│   ├── dashboard/
│   │   └── hitl.py
│   │
|   ├── evaluation/
│   │   ├── judge_evaluation.py
│   │   └── metrics.py
|── main.py
├── graph.py
├── run_evaluator.py
├──.gitignore
├── .env
├── requirements.txt
└── README.md
```

---

## Milestone 1: Basic Agent & Triage

In Milestone 1, the core email agent and workflow were implemented using **LangGraph**.

### What was implemented

* Designed the **state schema** to carry email data, decisions, and intermediate results across nodes.
* Implemented a **Triage Node** that classifies incoming emails into:

  * `ignore`
  * `notify_human`
  * `respond_or_act`
* Combined **rule-based triage** with **LLM-based fallback** to improve accuracy and generalization.
* Built the **ReAct Reasoning Node** to:

  * Think step-by-step (Reason)
  * Decide which tool to call (Act)
* Implemented **tool separation**:

  * Safe tools execute automatically
  * Dangerous tools (e.g., sending email) pause execution
* Added **Human-in-the-Loop (HITL)** dashboard and it create decison.json file where actions are saved.
* Verified agent execution by running `main.py` with a single email input.
* Enabled **LangSmith tracing** to visualize the graph execution and node-level behavior.

---

## Milestone 2: Evaluation Framework (LLM-as-a-Judge)

Milestone 2 focuses on measuring agent quality using a structured evaluation pipeline.

### What was implemented in

* Created a **golden evaluation dataset** (`.jsonl`) containing:

  * Email subject
  * Email body
  * Ideal (expected) response
* Defined a **Rulebook (`metrics.md`)** that specifies:

  * Quality criteria
  * Scoring rubric (1–5 scale)
  * Evaluation instructions for the judge LLM
* Implemented a custom **LangSmith RunEvaluator**(judge_evaluator.py):

  * `EmailJudgeEvaluator`
* Evaluation metrics:

  * Accuracy
  * Helpfulness
  * Tone
  * Safety
  * Conciseness
* Used a **single unified judge prompt** instead of multiple evaluators.
* Integrated evaluation with the existing agent graph **without modifying agent logic**.
* Ran batch evaluation using `run_evaluator.py`.

### How evaluation works

1. Each dataset email is passed through the agent.
2. The agent response is traced in LangSmith.
3. The evaluator LLM compares:

   * User email
   * Agent response
   * Ideal response
4. Scores are generated and logged automatically in LangSmith.

## Milestone 3: Human-In-The-Loop Handling

## Objective

Milestone 3 focuses on adding **Human-in-the-Loop (HITL)** control to the email assistant so that **dangerous actions are never executed automatically**.  
The system must pause, wait for human input, and resume safely.

---

## What Was Implemented

### End-to-End HITL Workflow

The agent now follows this flow:

1. Email is received  
2. Triage classifies the email  
3. Reasoning node decides an action  
4. Tool node checks if the action is dangerous  
5. **Execution pauses if approval is required**  
6. Human approves, edits, or denies  
7. Graph resumes and completes  
