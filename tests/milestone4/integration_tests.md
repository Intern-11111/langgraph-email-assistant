# Milestone 4 – Integration & Testing

## Test Case 1: Dangerous email approved
Input:
- Email requesting a refund

Expected:
- HITL pause triggered
- Tool executes after approval

Result:
- HITL pause observed
- Mock email tool executed
- Test passed

---

## Test Case 2: Dangerous email denied
Input:
- Email requesting a refund

Expected:
- HITL pause triggered
- Tool execution blocked

Result:
- HITL pause observed
- Tool not executed
- Test passed

---

## Test Case 3: Safe email
Input:
- Informational email

Expected:
- No HITL pause
- No tool execution

Result:
- Agent continued normally
- Test passed
