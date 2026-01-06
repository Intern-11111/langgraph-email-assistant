**Milestone 3 – Human-in-the-Loop (HITL)**

---

## 1. Overview

Milestone 3 introduces a **Human-in-the-Loop (HITL)** mechanism to the autonomous email assistant.  
The goal is to ensure that **critical or high-risk actions** are not executed autonomously and require **explicit human approval**.

This milestone uses **LangGraph interrupts** to pause the workflow when a dangerous action is detected.

---

## 2. Key Concepts

### Safe Tools
Safe tools are low-risk actions that can be executed autonomously.

- `read_email`
- `read_calendar`

### Dangerous Tools
Dangerous tools are actions with real-world impact and must require human approval.

- `send_email`
- `create_calendar_invite`

---

## 3. HITL Workflow

1. The agent selects a tool to execute.
2. The tool is checked against the dangerous tools list.
3. If the tool is **safe**:
   - Execution continues normally.
4. If the tool is **dangerous**:
   - The LangGraph workflow is interrupted.
   - Execution pauses.
   - Human approval is required.

This ensures safe and controlled autonomy of the agent.

---

## 4. Project Structure (Relevant Files)

langgraph-email-assistant/
│
├── src/
│ ├── tools_hitl.py # Safe and dangerous tool definitions
│ ├── hitl_guard.py # HITL interrupt logic
│ └── hitl_graph.py # LangGraph workflow with HITL
│
├── tests/
│ ├── test_safe_tool.py # Safe tool execution test
│ └── test_danger_tool.py # Dangerous tool interruption test
│
├── docs/
│ └── milestone3_report.md
│
├── app.py
├── .env
└── requirements.txt

---

## 5. How to Run Milestone-3 Tests

### Prerequisites
- Python 3.10+
- Virtual environment activated
- Dependencies installed
- `.env` file configured with LangSmith and LLM keys

---

### Run Safe Tool Test

From the project root:

python tests/test_safe_tool.py
Expected Output

SAFE TOOL OUTPUT: {
  'tool_name': 'read_calendar',
  'tool_input': '',
  'result': 'Calendar availability fetched.'
}
The workflow completes without interruption.

Run Dangerous Tool Test
From the project root:


python tests/test_danger_tool.py
Expected Behavior
Workflow pauses

Execution is interrupted

Human approval is required

Expected Output
bash
Copy code
DANGEROUS TOOL OUTPUT: {
  'tool_name': 'send_email',
  'tool_input': 'Project meeting confirmation',
  '__interrupt__': [...]
}
6. LangSmith Validation

LangSmith tracing is enabled to verify HITL behavior.

Observations
Safe tools complete execution normally.

Dangerous tools show:

Interrupted workflow

Paused execution

Awaiting human input

These traces confirm correct HITL enforcement.

7. Outcome

✔ Safe and dangerous tools identified

✔ HITL interrupt implemented successfully

✔ Dangerous actions blocked without approval

✔ LangSmith traces verified

✔ Milestone 3 completed successfully

8. Conclusion

Milestone 3 ensures safe autonomy by integrating a Human-in-the-Loop mechanism.
The agent is now capable of autonomous operation while maintaining human control over critical actions, making it suitable for real-world deployment in later milestones.

✅ **Milestone 3 Completed Successfully**