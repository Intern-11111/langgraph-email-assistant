# Milestone 3 – HITL Safety Testing and LangSmith Tracing

## Objective
The goal of Milestone 3 is to validate that the Human-in-the-Loop (HITL) safety mechanism works as expected and that LangSmith can trace the agent’s decision flow for debugging and observability.

This milestone focuses on testing safety behavior, not building a full production agent.

---

## Task 1: LangSmith Integration
LangSmith was connected using environment variables and the `@traceable` decorator.

The following were verified:
- Tracing is enabled using `LANGCHAIN_TRACING_V2=true`
- A dedicated project (`email-agent-hitl`) is used
- Function-level traces appear in the LangSmith UI

The traces show inputs, outputs, and execution flow for each decision step.

---

## Task 2: Test Case Design (Safe vs Dangerous)

The following test cases were designed conceptually:

### Dangerous Scenarios
These are actions that can affect users or systems and must pause for human review.
- Refund requests
- Account-related actions

Expected behavior:
- Classified as **dangerous**
- HITL pause is triggered

### Safe Scenarios
These are informational or low-risk emails.
- Meeting requests
- General queries
- Thank-you emails

Expected behavior:
- Classified as **safe**
- Execution continues without pause

---

## Task 3: HITL Pause Test Implementation
A test script was created to simulate the agent’s safety flow.

The test performs:
1. Classification of email content
2. Detection of dangerous actions
3. Triggering of HITL pause when required

LangSmith traces confirm:
- `decide_action_type` runs first
- `hitl_decision` runs next
- Dangerous inputs result in `paused_for_review`

A parent trace (`full_hitl_flow`) groups the entire execution.

---

## Observations
- HITL pause works correctly for dangerous actions
- Safe actions would continue execution
- LangSmith provides clear visibility into decision order and outcomes

---

## Limitations
- The test uses rule-based logic instead of a real LLM
- Only a limited number of test cases were manually simulated

---

## Conclusion
Milestone 3 successfully validates that the HITL safety mechanism and LangSmith observability work as intended. This provides a strong foundation for integrating a real agent and more advanced safety logic in future milestones.
