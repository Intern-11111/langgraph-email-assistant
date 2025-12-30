# Milestone-2: HITL Evaluation and Failure Analysis

## What this milestone is about

The purpose of this milestone is to check whether the Human-in-the-Loop (HITL)
framework designed in Milestone-1 is practically useful when the agent is
tested against different types of real email scenarios.

At this stage, the agent backend is not fully integrated.
So the evaluation is done by simulating how the agent would behave
and checking whether the HITL design is sufficient for safety,
control, and debugging.

---

## Dataset used

The dataset provided contains 100 email examples.
Each entry includes:
- Email category
- Email content
- Expected ideal response

The dataset covers different scenarios such as:
- Meeting requests
- Urgent queries
- Customer support emails
- Job inquiries
- Follow-ups
- Feedback
- Complaints
- Information requests
- Spam emails

This dataset is suitable for testing HITL behavior because it includes
both low-risk and high-risk email cases.

---

## How the evaluation was done

Since the agent logic is not yet connected to the UI,
the evaluation was done using a simulated run approach.

For each selected email:
- The intent of the email was understood
- A logical triage decision was assumed
- It was checked whether human approval should be required
- The clarity of explanation was evaluated
- The expected human action (Approve / Escalate) was identified

This approach helps in validating the HITL design without requiring
full automation.

---

## Sample evaluation cases

### Case 1: Urgent Query – Account Access Issue

**Email**
"My account is locked and I need immediate help."

**Expected Triage Decision**
Requires Human Approval

**Reason**
Account access issues can involve security risks and identity verification.

**HITL Action**
Escalate

**Observation**
The HITL framework correctly identifies this as a high-risk case.
However, the UI does not show any explicit security policy or confidence
level to help the human reviewer understand the severity.

---

### Case 2: Spam – Promotional Message

**Email**
"Congratulations! You won a prize. Click now."

**Expected Triage Decision**
Spam / No Action Required

**HITL Action**
No human intervention required

**Observation**
This case is safe to auto-handle.
However, there is no explanation shown about why it is classified as spam,
which reduces transparency for the reviewer.

---

### Case 3: Complaint – Incorrect Billing

**Email**
"Incorrect billing amount."

**Expected Triage Decision**
Requires Human Approval

**Reason**
Billing-related issues can impact customer trust and require verification.

**HITL Action**
Approve or Escalate based on investigation

**Observation**
The HITL step is necessary here.
The current framework allows human control,
but the explanation provided is minimal and does not justify the decision clearly.

---

### Case 4: Meeting Request

**Email**
"Can we schedule a meeting tomorrow at 3 PM?"

**Expected Triage Decision**
Auto-handle

**HITL Action**
No human intervention required

**Observation**
This is a low-risk case.
HITL is not required, and auto-handling is acceptable.
The framework supports this correctly.

---

### Case 5: Customer Support – Password Reset

**Email**
"Unable to reset my password."

**Expected Triage Decision**
Requires Human Approval

**Reason**
Password-related issues involve account security.

**HITL Action**
Escalate

**Observation**
HITL is required, but the framework does not currently show
why this case is more sensitive than general support emails.

---

## Summary of observations

Based on the evaluated cases:
- HITL is correctly required for urgent, account-related, and billing issues
- Low-risk emails like meeting requests and spam can be auto-handled
- The UI structure supports human approval and escalation
- Explanation clarity is limited
- No confidence score or risk indicator is shown to the human reviewer

---

## Failure analysis

The following gaps were observed:
- No visibility into how confident the agent is about its decision
- Explanations are short and not always sufficient for human judgment
- No clear policy rules are shown in the UI
- Human reviewers do not get enough context to understand why a decision was made

These are not execution errors but design limitations at this stage.

---

## Root cause diagnosis

The identified gaps exist because:
- Agent reasoning logic is not yet integrated
- LangSmith tracing is configured but not connected to real execution
- The current evaluation is manual and conceptual
- Risk policies are not explicitly defined in the system

---

## Role of LangSmith in this milestone

LangSmith was set up during Milestone-1 to support observability.

In the current milestone, LangSmith is not actively logging traces because
the agent execution pipeline is not connected yet.

In future milestones, LangSmith will be used to:
- Log triage decisions
- Capture reasoning steps
- Record human approval or escalation actions
- Support failure analysis and debugging

---

## Conclusion

This milestone confirms that the HITL framework is structurally ready
to support safe AI decision-making.

While full automation is not yet implemented,
the design allows humans to intercept risky cases
and provides a foundation for observability and debugging.

The evaluation highlights areas that need improvement in future milestones,
especially explanation quality and policy visibility.
