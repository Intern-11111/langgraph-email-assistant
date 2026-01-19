# Milestone 3 – HITL Safety, Tracing, and Test Validation

## Objective

The goal of Milestone 3 is to verify that the Human-in-the-Loop (HITL) safety mechanism works correctly for dangerous actions and that LangSmith captures the complete decision flow for debugging and observability.

This milestone focuses on **safety validation**, not on building a full production-ready agent.

---

## LangSmith Integration

LangSmith tracing was enabled using environment variables and the `@traceable` decorator.

Each major decision step in the HITL flow is recorded as a trace.  
To clearly visualize execution order, a parent trace named `full_hitl_flow` was created to group the following child steps:

- `decide_action_type`
- `hitl_decision`

This structure allows the complete HITL decision flow to be observed inside the LangSmith dashboard.

---

## Test Case Design

Test cases were designed based on **action risk**, rather than dataset size.

### Dangerous Cases
- Emails involving refunds or account-related actions
- These actions can modify system state and must not execute automatically

### Safe Cases
- Informational emails without side effects
- These actions do not require human intervention

This approach ensures HITL safety behavior is tested without requiring a fully integrated backend agent.

---

## HITL Pause Validation

### For Dangerous Emails
- The agent classifies the action as dangerous
- Execution pauses at the HITL checkpoint
- The system waits for explicit human approval

### For Safe Emails
- The agent continues execution without interruption

These behaviors were verified using both console output and LangSmith traces.

---

## Observability Results

LangSmith successfully captured the following:

- Inputs and outputs for each decision step
- Parent-child execution order
- HITL pause state for dangerous actions

This confirms that the system behavior is both **auditable** and **debuggable**.

---

## Limitations

- Agent logic is simulated and does not execute real tools
- No memory persistence or resume logic is implemented in this milestone

These limitations are intentional and will be addressed in Milestone 4.

---

## Conclusion

Milestone 3 successfully validates HITL safety behavior and observability.  
The system correctly pauses before dangerous actions and records the full decision flow in LangSmith, meeting all milestone requirements.
