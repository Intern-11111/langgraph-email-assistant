# Milestone 4 — Human-in-the-Loop Incoming Email Assistant

## Overview
Milestone 4 implements a human-in-the-loop (HITL) assistant for processing incoming emails. The system classifies each email as one of:
- Denied (spam): Automatically blocked and not processed
- Needs-human (sensitive): Pauses before processing and requests human approval/denial/edits
- Approved (non‑sensitive): Automatically processed without interruption

This milestone demonstrates clear user notifications, safe interruption points, state inspection and update, and resuming execution with the updated state. It also includes a simple evaluation script and achieves a quality rate (accuracy) of ~90% on the provided labeled dataset.

## Architecture
- [Milestone4/agent.py](agent.py)
  - Node `email_agent(state)` constructs an initial `email_data` draft from the provided `input` and returns it into the graph state.
- [Milestone4/graph.py](graph.py)
  - Defines `EmailState` (TypedDict) to ensure values aggregate across nodes.
  - Node `review_node(state)` classifies the email using tuned keyword rules into `review_status ∈ {denied, needs-human, approved}`.
  - Node `send_email_node(state)` acts as an incoming email handler:
    - Skips processing for `denied` with a clear reason banner
    - Processes otherwise (prints a structured summary)
  - Graph flow: `agent → review → tools → END`.
- [Milestone4/tools.py](tools.py)
  - `mock_send_email(data)` renamed in semantics to an incoming email handler; prints ROUTE/ SUBJECT/ BODY/ ACTION and returns a status.
- [Milestone4/main.py](main.py)
  - CLI for end‑to‑end runs. Key capabilities:
    - Auto detection (spam / sensitive / non‑sensitive) from subject+body (or input)
    - Auto‑pause before processing when sensitive (`needs-human`)
    - Clear, step‑by‑step narration (Configuration → Review & Pause → Human Decision → Process → Outcome)
    - Prominent sensitive alert with matched keywords
    - Interactive decision at pause: Approve, Deny, or Edit (edits applied before processing)
- [Milestone4/evaluate.py](evaluate.py)
  - Evaluates the detection rules on [data/golden_emails.json](../data/golden_emails.json)
  - Maps labels: `spam → denied`, `finance → needs-human`, all others → `approved`
  - Reports overall accuracy (“quality rate”), per‑class totals, and a confusion matrix

## Key Behaviors
- Non‑Sensitive (approved)
  - No pause; processed automatically
  - Handler prints a structured summary and returns `Email Processed`
- Sensitive (needs‑human)
  - Auto‑pause before processing
  - Prints a prominent alert and the matched sensitive keywords
  - Interactive decision:
    - Approve → proceed without changes
    - Edit → prompt for `TO / SUBJECT / BODY`; updates are applied before processing
    - Deny → mark `review_status=denied` and skip processing
- Spam (denied)
  - No pause; classification is `denied`
  - Prints `INCOMING EMAIL SKIPPED` and returns `Denied - Not Processed`

## Deliverables Mapping
- Clear notifications: Step‑by‑step narration and banners (alerts and skip reasons) in the CLI.
- HITL pause and resume: Sensitive emails auto‑pause; the CLI prompts for Approve/Deny/Edit, then resumes accordingly.
- State inspection and update prior to processing:
  - The CLI retrieves graph state at the pause (review status, draft), applies updates (edits), and resumes so the handler uses the modified draft.

## Try It (CLI Examples)
Run from repository root on Windows (adjust interpreter path if needed):

- Non‑sensitive (approved; no pause)
```
python.exe Milestone4\main.py --input "Please send the weekly team update" --email-subject "Weekly Team Update" --email-body "Please share the weekly team update by EOD."
```

- Sensitive (auto‑pause; decide Approve / Deny / Edit)
```
python.exe Milestone4\main.py --input "Please approve the internship" --email-subject "Internship Approval" --email-body "Respected Sir, kindly approve my internship request."
```

- Spam (denied; no pause)
```
python.exe Milestone4\main.py --input "Congratulations! Click here to claim your prize" --email-subject "Limited Time Offer" --email-body "Act now, click the link to get your free gift."
```

## Evaluation (“Quality Rate”)
- Script: [Milestone4/evaluate.py](evaluate.py)
- Dataset: [data/golden_emails.json](../data/golden_emails.json)
- Run:
```
python.exe Milestone4\evaluate.py
```
- Current result (at the time of writing):
  - Quality rate (accuracy): ~90%
  - Balanced performance with improved sensitive recall and fewer promotion false positives

## Design Notes
- Rules first: The milestone uses transparent keyword rules for spam/sensitivity to make HITL and behavior easy to verify and adjust.
- Typed state: `EmailState` (TypedDict) helps LangGraph aggregate values cleanly across nodes.
- Incoming semantics: The flow models received email processing (skip/process), not sending. Banners, action labels, and outcome text reflect this.

## Extensibility
- Externalize rules: Move spam/sensitive keyword lists to a JSON/TOML config and load at runtime.
- Logging/reporting: Add a `--log` flag in the CLI to persist outcomes (status, review, edits) per thread/session.
- Unit tests: Codify sticky examples (CTAs without prizes, finance messages without classic keywords) to prevent regressions.

---
If you want this README to include screenshots or sample outputs, I can capture a few runs and embed them here.