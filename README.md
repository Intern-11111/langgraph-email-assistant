# LangGraph Email Assistant with HITL Safety

This project focuses on building a **Human-in-the-Loop (HITL)** framework for an AI email assistant using **LangGraph concepts**.

The work is divided into milestones, where each milestone focuses on a specific part of **safety, control, testing, and integration**.

The goal is **not** to build a full production agent immediately, but to **design, validate, and test safety mechanisms step by step**.

---

## 🧩 Project Structure

email-agent-project/
│
├── dashboard/ # HITL UI skeleton (Milestone 1)
├── src/ # Core HITL logic and mock tools
│ ├── hitl.py
│ └── tools.py
│
├── tests/
│ ├── milestone3/ # HITL safety tests + report
│ └── milestone4/ # Integration & testing docs
│
├── main.py # Final integration script
├── README.md # Project documentation
├── milestone2_evaluation.md # Milestone 2 analysis
└── .env # Environment variables (ignored in Git)


---

## 🚩 Milestone 1 – HITL Design & UI Skeleton

### Objective
The objective of Milestone 1 was to **design the Human-in-the-Loop (HITL) concept** and create a **basic UI skeleton** that shows how human review happens before dangerous actions.

This milestone focuses on **design and structure**, not backend execution.

### What Was Done
- Identified **dangerous actions** such as:
  - Sending emails
  - Modifying account data
  - Performing irreversible actions
- Understood the **Undo Test**:
  - If an action changes reality → dangerous
  - If it only reads data → safe
- Designed a **HITL checkpoint**
- Created a **basic HITL review UI skeleton** with:
  - Approve
  - Deny
  - Edit (future scope)

### Deliverables
- `dashboard/hitl_review.py`
- HITL flow design
- Clear separation of safe vs dangerous actions

### Outcome
This milestone establishes **where and why human approval is required**.

---

## 🚩 Milestone 2 – HITL Evaluation & Failure Analysis

### Objective
The objective of Milestone 2 was to **evaluate the HITL framework** using real-world email scenarios and analyze **failure cases**, even though the backend agent was not integrated yet.

### What Was Done
- Reviewed **100+ email examples**
- Simulated how the agent **would behave**
- Evaluated:
  - When HITL should trigger
  - Where unsafe actions could occur
- Identified failure patterns such as:
  - Ambiguous requests
  - Urgent language
  - Missing context

### Important Note
At this stage:
- Backend execution is **not connected**
- Evaluation is **analytical and design-based**
- This is intentional

### Deliverables
- `milestone2_evaluation.md`
- Failure analysis and observations

### Outcome
Milestone 2 confirms the **need for strict HITL safeguards**.

---

## 🚩 Milestone 3 – HITL Safety, Tracing & Test Validation

### Objective
The objective of Milestone 3 was to **technically validate** that:
1. Dangerous actions are detected
2. HITL pause is triggered
3. LangSmith captures the **full decision flow**

This milestone focuses on **safety validation and observability**.

---

### LangSmith Integration
- Enabled LangSmith tracing using environment variables
- Used `@traceable` decorator
- Created a **parent trace** (`full_hitl_flow`) to group steps:
  - `decide_action_type`
  - `hitl_decision`

This allows the **execution order** to be visualized.

---

### Test Case Design
**Dangerous cases**
- Refund requests
- Account-related actions

**Safe cases**
- Informational emails with no side effects

---

### HITL Pause Validation
For dangerous emails:
- Action classified as dangerous
- Execution pauses
- System waits for human approval

For safe emails:
- Execution continues normally

These behaviors were verified through:
- Console output
- LangSmith traces

---

### Deliverables
- `tests/milestone3/hitl_test.py`
- `tests/milestone3/report.md`
- Verified traces in LangSmith

---

### Outcome
Milestone 3 proves:
- HITL pauses correctly
- Dangerous actions never auto-execute
- Decision flow is fully traceable

---

## 🚩 Milestone 4 – HITL Integration & Mock Tool Testing

### Objective
The objective of Milestone 4 was to **integrate HITL logic** with **mock tools** and test end-to-end behavior safely.

---

### What Was Implemented
- Mock tools (example: `send_email`)
- HITL decision handler:
  - Approve → tool executes
  - Deny → execution blocked
- Clear user alerts during HITL pause
- Final integration flow in `main.py`

---

### Integration Flow
1. Email received
2. Action type detected
3. HITL pause triggered
4. Human decision simulated
5. Tool executes only after approval

---

### Testing
- Verified approval path
- Verified denial path
- Verified correct tool execution

---

### Deliverables
- `src/hitl.py`
- `src/tools.py`
- `main.py`
- `tests/milestone4/integration_tests.md`

---

## ✅ Overall Conclusion

Across all four milestones:
- HITL safety is **designed, tested, traced, and integrated**
- Dangerous actions never execute without approval
- System behavior is observable via LangSmith
- Architecture is clean and extensible

This project provides a strong foundation for a **safe and auditable AI email assistant**.

