# Milestone 3 – Human-in-the-Loop (HITL) Implementation

## 1. Objective

The objective of Milestone 3 is to implement a **Human-in-the-Loop (HITL)** mechanism that ensures the autonomous email agent does not execute **critical or risky actions** without explicit human approval.

This milestone focuses on introducing controlled autonomy by pausing the agent’s workflow whenever a dangerous action is detected and waiting for human intervention before proceeding.

---

## 2. Safe and Dangerous Tools Classification

To enforce HITL, tools used by the agent are classified into **safe** and **dangerous** categories.

### 2.1 Safe Tools
Safe tools are low-risk actions that can be executed autonomously without human approval.

- `read_email`
- `read_calendar`

These tools execute normally and do **not trigger** the HITL mechanism.

---

### 2.2 Dangerous Tools
Dangerous tools are actions that may have real-world consequences and therefore **must require human approval**.

- `send_email`
- `create_calendar_invite`

Whenever these tools are triggered, the agent workflow must pause.

---

## 3. HITL Design and Logic

The HITL mechanism is implemented using **LangGraph interrupts**.

### Workflow Logic:
1. The agent selects a tool to execute.
2. Before execution, the tool name is checked.
3. If the tool is classified as **dangerous**:
   - The LangGraph workflow is interrupted.
   - Execution pauses.
   - Human approval is required.
4. If the tool is **safe**:
   - The workflow continues without interruption.

This approach ensures safe and controlled autonomy of the agent.

---

## 4. Implementation Overview

### Files Added for Milestone 3:
- `src/tools_hitl.py` – Defines safe and dangerous tools
- `src/hitl_guard.py` – Implements HITL interrupt logic
- `src/hitl_graph.py` – LangGraph workflow with HITL checkpoint
- `tests/test_safe_tool.py` – Test case for safe tool execution
- `tests/test_danger_tool.py` – Test case for dangerous tool interruption

All existing Milestone-1 and Milestone-2 files were left unchanged.

---

## 5. Test Cases and Results

### 5.1 Test Case 1 – Safe Tool Execution

**Tool:** `read_calendar`  
**Expected Behavior:**
- Tool executes automatically
- No interruption

**Observed Output:**


**Result:** ✅ Passed

SAFE TOOL OUTPUT: {
'tool_name': 'read_calendar',
'tool_input': '',
'result': 'Calendar availability fetched.'
}

---

### 5.2 Test Case 2 – Dangerous Tool Execution

**Tool:** `send_email`  
**Expected Behavior:**
- Workflow pauses
- Human approval required

**Observed Output:**

**Result:** ✅ Passed

DANGEROUS TOOL OUTPUT: {
'tool_name': 'send_email',
'tool_input': 'Project meeting confirmation',
'interrupt': [
Interrupt(
value={
'reason': 'Dangerous tool detected',
'tool': 'send_email',
'input': 'Project meeting confirmation',
'action_required': 'Human approval needed'})]}

---

## 6. LangSmith Validation

LangSmith tracing was enabled to validate HITL behavior.

### Observations:
- Safe tools complete execution normally.
- Dangerous tools show:
  - `interrupted` state
  - Paused workflow
  - Awaiting human input

These traces confirm correct HITL enforcement.

---

## 7. Conclusion

Milestone 3 was successfully completed by implementing a **Human-in-the-Loop checkpoint** using LangGraph. The agent now:

- Executes safe actions autonomously
- Pauses on dangerous actions
- Requires human approval before executing critical operations

This ensures safe autonomy and prepares the system for real-world deployment.

---

## 8. Final Outcome

- ✔ Safe and dangerous tools identified  
- ✔ HITL interrupt implemented successfully  
- ✔ Dangerous actions blocked without approval  
- ✔ LangSmith traces verified  
- ✔ Milestone 3 objectives achieved  

---
