
# Human-In-The-Loop- Milestone 3

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

---

### Dangerous Tool Identification

Actions that can cause irreversible effects are marked as **dangerous**, such as:

* Sending emails  
* Replying to emails  
* Deleting emails  
* Creating calendar events  

These actions **always require human approval**.

---

### Graph Interrupt & Resume

* LangGraph checkpointing is used  
* Execution pauses **before tool execution**  
* State is saved safely  
* The graph resumes exactly where it stopped after human input  

---

### Human Decision Handling

The human reviewer can:

* **Approve** – execute the action as-is  
* **Edit** – modify the content and then execute  
* **Deny** – stop execution completely  

Each decision updates the system state and database.

---

### Persistent Storage

* Emails and edits are stored in a JSONL database /file  
* Agent state survives pauses  
* Ensures reliability and traceability  

---

### Streamlit HITL Interface

A simple UI was built to:

* Submit emails  
* Display HITL pause  
* Collect human decisions  
* Resume execution  

This simulates real-world review workflows.

---

## Core Functions & Their Responsibilities

### `save_email()`

* Stores incoming emails in persistent storage  
* Assigns a unique ID to each email  
* Ensures traceability across pauses and resumes  

---

### `update_email()`

* Updates email status (`PENDING`, `APPROVED`, `DENIED`, `EDITED`)  
* Stores edited content when human modifies an action  
* Maintains audit history  

---

### `TriageNode.__call__()`

* Acts as the **gatekeeper** of the system  
* Classifies emails into:
  * `ignore`
  * `notify_human`
  * `reason_act`
* Prevents unnecessary LLM calls and unsafe execution  

---

### `ReasonNode.__call__()`

* Executes only when triage result is `reason_act`  
* Analyzes email content  
* Chooses the next action and its parameters  
* Produces a structured reasoning output  

---

### `ToolExecutorNode.__call__()`

* Detects whether an action is **safe or dangerous**  
* Triggers HITL pause for dangerous tools  
* Executes safe tools automatically  
* Applies human decisions (approve/edit/deny)  

---

### `execute_tool()`

* Contains actual execution logic for tools  
* Runs only after safety checks or approval  
* Returns execution results back to the graph  

---

## Key Outcomes

* No dangerous action executes without approval  
* Agent can pause and resume safely  
* Human edits are applied correctly  
* System is stable and production-ready  
* Full audit trail via stored state  
