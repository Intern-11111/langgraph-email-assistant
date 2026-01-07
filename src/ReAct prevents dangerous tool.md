# ReactAgent with Human-in-the-Loop (HITL)

## Overview

This module implements a **ReAct-style email agent** with **Human-in-the-Loop (HITL)** control. The agent can:

* Analyze incoming emails
* Decide an action (reply, lookup contact, create calendar event)
* **Pause execution for sensitive actions**
* Resume only after explicit human approval
* Maintain a full execution trace for debugging and auditing

This design is suitable for enterprise workflows where AI autonomy must be controlled.

---

## Key Concepts

### ReAct Pattern

ReAct = **Reason + Act**

The agent iteratively:

1. Thinks about the next step (reasoning)
2. Chooses an action
3. Executes a tool or responds
4. Logs everything in a trace

---

## File Responsibilities

### Imports

```python
import json
import time
from typing import Dict, Any, List
from langsmith import traceable

from tools.calendar import read_calendar, create_event
from tools.contact import lookup_contact
```

* `json`: parse/edit human input
* `time`: timestamps + trace IDs
* `typing`: type safety
* `langsmith.traceable`: observability (optional but recommended)
* `tools.*`: mock tools used by the agent

---

## Sensitive Action Control

```python
SENSITIVE_ACTIONS = {"send_email", "spend_money", "create_event"}
```

These actions **must not run automatically**.

### Helper Function: `is_sensitive_action`

```python
def is_sensitive_action(action: str) -> bool:
    return action in SENSITIVE_ACTIONS
```

**Purpose:**

* Centralized safety check
* Keeps business rules out of agent logic

---

## Intent Classification Helper

### `decide_action()`

```python
def decide_action(subject: str, body: str) -> tuple[str, Any]:
```

**Responsibility:**

* Reads email subject + body
* Decides what the agent should do

#### Logic

| Condition                        | Action           |
| -------------------------------- | ---------------- |
| Contains `schedule` or `meeting` | `create_event`   |
| Contains `contact` or `email`    | `lookup_contact` |
| Otherwise                        | `reply`          |

This is a **rule-based stand-in** for an LLM decision step.

---

## ReactAgent Class

### Initialization

```python
class ReactAgent:
    def __init__(self, max_steps: int = 6):
        self.max_steps = max_steps
```

Limits how many ReAct steps can execute.

---

## Core Method: `run()`

```python
def run(self, subject, body, context=None, human_decision=None)
```

### Inputs

| Parameter        | Description                             |
| ---------------- | --------------------------------------- |
| `subject`        | Email subject                           |
| `body`           | Email body                              |
| `context`        | Optional metadata                       |
| `human_decision` | Approval / deny / edit (used on resume) |

---

### Trace Structure

```python
agent_trace = {
  "input": {...},
  "trace": [],
  "final": {},
  "status": "RUNNING"
}
```

This ensures **full transparency** of agent behavior.

---

### Step Loop

```python
for step in range(1, self.max_steps + 1):
```

Each iteration represents one ReAct cycle.

---

### Reasoning Step

```python
thought = "Analyzing email intent and deciding next action"
action, action_input = decide_action(subject, body)
```

* Mimics LLM reasoning
* Determines next tool or reply

---

### HITL Pause Check (Critical)

```python
if is_sensitive_action(action) and human_decision is None:
```

If the action is sensitive:

* Execution **pauses immediately**
* No tool is executed
* State is safely returned

```json
"status": "PAUSED"
```

---

### Human Decision Handling

```python
if human_decision:
    decision = human_decision.get("decision")
```

| Decision  | Effect             |
| --------- | ------------------ |
| `approve` | Continue execution |
| `deny`    | Stop permanently   |
| `edit`    | Modify tool input  |

This logic ensures **human authority** over AI actions.

---

### Tool Execution

```python
if action == "lookup_contact":
    observation = lookup_contact(action_input)
```

Supported tools:

* `read_calendar`
* `lookup_contact`
* `create_event`
* `reply` (no external tool)

---

### Termination Condition

```python
if action == "reply":
    agent_trace["status"] = "COMPLETED"
```

Reply ends the agent lifecycle.

---

## Resume Method (HITL)

### `resume()`

```python
def resume(self, paused_trace, human_decision=None)
```

### Purpose

* Resume **only PAUSED traces**
* Apply human decision safely

---

### Interactive Mode

If `human_decision` is not passed:

* Prompts human via CLI
* Accepts Approve / Deny / Edit
* Allows JSON editing of input

---

### Safe Re-entry

```python
return self.run(..., human_decision=human_decision)
```

The agent **re-enters through the same logic**, preserving safety.

---

## Example Execution Flow

1. Email requests meeting
2. Agent decides `create_event`
3. Action is sensitive → PAUSE
4. Human reviews details
5. Human approves
6. Event is created
7. Trace marked COMPLETED

---

## Why This Design Is Correct

* ✅ Prevents unauthorized actions
* ✅ Fully auditable
* ✅ Extensible to real LLMs
* ✅ Enterprise-ready HITL workflow

---

## Next Improvements

* Replace `decide_action()` with LLM
* Persist traces to database
* Web-based approval UI
* Role-based approvers

---

## Summary

This implementation demonstrates a **production-grade ReAct agent** with:

* Deterministic reasoning
* Human safety checkpoints
* Resume-only-after-approval guarantees

Perfect for milestone-based AI systems and compliance-heavy environments.
