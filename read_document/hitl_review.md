# HITL (Human-in-the-Loop) Review App

This Streamlit application demonstrates a **Human-in-the-Loop (HITL)** workflow for reviewing AI/agent email triage decisions. It loads emails from a JSON dataset, displays the agent's classification and reasoning, and allows a human reviewer to **Approve** or **Escalate** the decision.

---

## Purpose

* Simulate an AI-assisted email triage system
* Show how **human oversight** can be added before taking final action
* Log human decisions for auditing and improvement

---

## 🛠 Tech Stack

* **Python**
* **Streamlit** – UI for human review
* **JSON** – Dataset & decision storage

---

## Project Structure

```text
project/
│
├── decision.json               # Stored human decisions (auto-created)
└── src/
    └── data/
        └── emails.json   # Email dataset
        └── dashboard/
        └── hitl.py       #streamlit HITL UI
```

---

## Email Data Format (`emails.json`)

Each email in the dataset should follow this structure:

```json
{
  "subject": "Account Verification Required",
  "body": "Please verify your account immediately...",
  "sender": "security@example.com",
  "human_label": "phishing"
}
```

---

## Application Workflow

### 1. Load Email

* Randomly selects an email from the dataset
* Extracts subject, body, sender, and label

### 2. Triage Simulation

* Uses dataset label as triage output
* Generates a **fake confidence score** (0.75–0.98)

### 3. ReAct Trace (Explainability)

Shows agent reasoning steps such as:

* Classification decision
* Action taken
* Observation

### 4. Human Decision

* **Approve** → Accept agent decision
* **Escalate** → Flag for further review

### 5. Decision Logging

Each action is stored in `decision.json` with:

* Timestamp
* Decision type
* Full email + triage data

---

## Key Functions

### `load_pending_email()`

* Reads email dataset
* Converts it into a HITL-compatible structure

### `save_decision(decision, data)`

* Appends human decision to `decision.json`
* Useful for audits and training feedback loops

---

## How to Run

1. Install dependencies:

```bash
pip install streamlit
```

1. Run the app:

```bash
streamlit run hitl.py
```

1. Open browser at:

<http://localhost:8501>

---

## Features

* Clean human review UI
* Transparent agent reasoning
* Persistent decision logging
* Simple and extensible HITL design
