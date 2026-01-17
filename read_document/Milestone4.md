# Email Assistant with Human-in-the-Loop (HITL)

## Milestone 4 Objectives

### Resume Logic

* The agent graph **pauses execution** when a dangerous tool is detected.
* After human input (approve / edit / deny), the graph **resumes from the same state**.
* Implemented using:

  * `interrupt_before=["tool"]`
  * `MemorySaver()` for checkpointing
  * Consistent `thread_id` for resumption

---

### Agent Draft Modification (HITL)

* The agent’s proposed action and draft are saved.
* Human can:

  * **Approve** the draft
  * **Edit** the draft (modified content replaces agent output)
  * **Deny** the action completely
* Final execution always respects the human decision.

---

### Integration & Mock Tool Testing

* All tools are **mocked** to ensure safety.
* Supported actions include:

  * `send_email`
  * `reply`
  * `delete_email`
  * `create_calendar_event`
  * `lookup_contact`
* No real emails or calendar events are triggered.

---

### Edge Case Handling

* Human rejection stops execution.
* Edited content is used instead of agent draft.
* Tool execution happens **only once**.
* Safe tools bypass HITL.
* System waits safely when no human decision is provided.

---
---

## main4.py (Assembly File)

`main4.py` is the **final assembly file** for Milestone 4. It:

* Builds the HITL graph
* Runs multiple test scenarios
* Demonstrates pause and resume logic
* Uses **terminal-based HITL** instead of UI

### Features Demonstrated in `main4.py`

* Dangerous actions trigger HITL pause
* Human approval/edit/deny via terminal input
* Graph resumes with the same `thread_id`
* Safe actions execute without interruption

---

## Email Storage (emails.jsonl)

The system uses a lightweight file-based database named emails.jsonl to store all email-related actions and state transitions.

Each line in the file represents a single email record in JSON format.

### Stored Information Includes

* Email ID
* Subject and body
* Agent-generated draft
* Human-edited content (if any)
* Current status (CREATED, WAITING_FOR_APPROVAL, APPROVED, EDITED, DENIED)
* Tool execution history
* Timestamps for creation and updates

### This file enables

* Auditability of agent and human actions
* Verification of HITL decisions
* Testing and debugging of edge cases

## Edge Case Testing

### Edge Case 1: Human Denies Action

* Action: `send_email`
* Human chooses **Deny**
* Tool is NOT executed
* Status set to `DENIED`

**Result:** PASS

---

### Edge Case 2: Human Edits Draft

* Agent proposes message
* Human edits content
* Edited message replaces agent draft
* Tool executes with edited input

**Result:** PASS

---

### Edge Case 3: Resume After Interruption

* Graph pauses at tool node
* Human approves action
* Graph resumes from checkpoint
* Tool executes once

**Result:** PASS

---

### Edge Case 4: Duplicate Execution Prevention

* Application rerun after execution
* `_tool_executed` flag prevents re-run

**Result:** PASS

---

### Edge Case 5: Safe Tool (No HITL)

* Action: `lookup_contact`
* No interruption
* Tool executes immediately

**Result:** PASS

---

## How to Run

### Run Milestone 4 Demo (Terminal-Based)

```bash
python main4.py
```

### Run Streamlit UI

```bash
streamlit run src/HITL/hitl_app.py
```

---

## Deliverables Summary

* ✅ Resume-capable LangGraph
* ✅ Human approval/edit/deny logic
* ✅ Agent draft persistence
* ✅ Mock tool execution
* ✅ Edge case testing
* ✅ Final assembly via `main4.py`
