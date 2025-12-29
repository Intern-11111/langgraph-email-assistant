---

# LangGraph Email Assistant

A smart email triage and automation system powered by **LangGraph**, **LangChain**, **FastAPI**, and **Hugging Face Transformers**.

---

## Milestone 1 — Core System Setup & Basic Email Triage Agent

### Goal of Milestone 1

Establish the foundation required for building a fully autonomous email assistant:

* Setup Python environment & architecture
* Validate AI framework compatibility
* Build basic triage logic for email routing
* Enable experimental evaluation via APIs

---

## Key Contributions

###  1️⃣ Environment & Infrastructure (Developer: Lead Responsibility)

The development environment was fully prepared including:

* Virtual environment configuration (`venv`)
* Installation of all key dependencies
* `.gitignore` rules to exclude:

  * `venv/`, `.env`, cache folders, temporary artifacts
* Modular project structure designed for future scalable growth

**Verified Libraries**

| Library      | Purpose                         |
| ------------ | ------------------------------- |
| langchain    | Prompt orchestration            |
| langgraph    | State machine for agent control |
| transformers | LLM model execution (TinyLlama) |
| fastapi      | Backend API                     |
| uvicorn      | Server for local testing        |
| datasets     | Loading evaluation dataset      |

---

### 2️⃣ Email Triage Agent

The first version of the intelligent agent uses logical heuristics to classify incoming emails into three triage categories:

| Category         | Meaning                          | Action                |
| ---------------- | -------------------------------- | --------------------- |
| **ignore**       | Spam, marketing, irrelevant      | Drop silently         |
| **notify_human** | Ambiguous, risky, legal concerns | Alert a human         |
| **respond**      | Routine business queries         | Auto-reply generation |

#### Agent Flow

```
Incoming Email 
        ↓
   TRIAGE NODE (decision logic)
        ↓
 Respond? ——— Yes → React Node (draft reply)
        ↓
  Final Output → response + reasoning
```

Components Built:

* **Triage Node**

  * Keyword pattern heuristics
  * Risk scoring
* **ReAct Draft Reply Node**

  * Generates polite short email replies using LLM

---

###  3️⃣ Evaluation & Demo

✔ Integrated dataset:
`SetFit/enron_spam` from Hugging Face

✔ Full evaluation tooling added:

* Accuracy measurement
* Ground-truth comparison for triage decisions
* Logging reason behind predictions

✔ FastAPI endpoints implemented:

| Endpoint | Description                  |
| -------- | ---------------------------- |
| `/eval`  | Run evaluation benchmark     |
| `/run`   | Test with custom input email |

Example output:

```json
{
  "triage_decision": "respond",
  "draft_reply": "Sure, happy to assist! Can you clarify…?",
  "reason": "Heuristic analysis of business coordination intent"
}
```

---

##  Project Structure

```
langgraph-email-assistant/
│
├── src/
│   ├── api/             # FastAPI routes + LLM provider
│   ├── graph/           # LangGraph build + agent state
│   ├── triage/          # Email triage logic
│   ├── agents/          # ReAct agent behavior
│   ├── utils/           # Support helpers
│
├── data/                # Datasets + test corpora
├── results/             # Outputs generated from evaluation
│
├── run_server.py        # Local API entry point
├── requirements.txt     # Dependencies list
├── README.md            # Project documentation
├── env_setup.md         # Setup instructions
└── .gitignore           # Ignore unnecessary files
```

---

##  Status of Milestone 1

| Feature                  | Status        |
| ------------------------ | ------------- |
| Env setup                |   Done        |
| Model integration        |   Done        |
| LangGraph pipeline       |   Done        |
| Heuristic triage         |   Done        |
| Evaluation + API         |   Done        |
| Ready for next milestone |   Approved    |

---
---

#  **Milestone 2 – Agent Evaluation & Quality Metrics**

##  Objective

Evaluate the LangGraph-based Email Triage Agent using structured datasets and measure accuracy, decision quality, and behavior across key email categories:

* **Respond** (coordination, confirmations)
* **Notify Human** (legal, financial, escalation)
* **Ignore** (spam, ads, phishing)

---

##  **Dataset Overview**

We constructed the evaluation dataset in **3 batches** aligned with triage decisions:

| Batch       | Dataset File                     | Category     | Count | Description                                  |
| ----------- | -------------------------------- | ------------ | ----: | -------------------------------------------- |
| **Batch 1** | `m2_testset_batch1_respond.json` | Respond      |   ~40 | Valid normal communication requiring a reply |
| **Batch 2** | `m2_testset_batch2_notify.json`  | Notify Human |   ~40 | Risk-sensitive content requiring escalation  |
| **Batch 3** | `m2_testset_batch3_ignore.json`  | Ignore       |   ~40 | Spam, marketing, phishing, irrelevant        |

 Total dataset size evaluated: **121 emails**

---

##  Evaluation Implemented

The endpoint:

```
GET /eval/evaluate
```

✔ Runs graph on entire dataset
✔ Computes classification correctness
✔ Scores reply quality for respond-case emails
✔ Writes results to:

 `/results/m2_eval_report.json`

---

##  Metrics Measured

| Metric                        | Purpose                               | Scale |
| ----------------------------- | ------------------------------------- | ----- |
| **Accuracy**                  | Correct triage decisions              | 0–1   |
| **Triage Score**              | Direct match to ideal label           | 0–1   |
| **Reply Quality Score**       | Relevance, keyword overlap            | 0–1   |
| **Tone Score**                | Courtesy markers (please/thanks etc.) | 0–1   |
| **Format Score**              | Decision validity                     | 0–1   |
| **Latency Score**             | Response speed                        | 0–1   |
| **Hallucination Score**       | Staying inside context                | 0–1   |
| **Agent Quality Score (AQS)** | Weighted overall quality              | 0–1   |

**AQS = Weighted combination of above dimensions**

---

## Milestone-2 Results (Summary)

| Metric                                |    Result |
| ------------------------------------- | --------: |
| **Total Emails Evaluated**            |       121 |
| **Correct Predictions**               |        54 |
| **Overall Accuracy**                  | **44.6%** |
| **Average Agent Quality Score (AQS)** |  **0.43** |

---

## Observations

✔ **Notify Human** and **Ignore** detection using heuristics works well
✔ Spam / risky content classification is reliable
✔ Respond-case emails lack strong reasoning → Many false escalations

⚠ **Latency extremely high** (CPU inference with 1.1B model)
⚠ Misclassification for short casual requests ("Can we talk?")
⚠ Reply generation too generic (low overlap score)

---

## Deliverables Completed in M2

| Feature                               | Status |
| ------------------------------------- | :----: |
| Graph agent integrated with evaluator |    ✅   |
| Test dataset ingestion                |    ✅   |
| Scoring system implementation         |    ✅   |
| JSON evaluation export                |    ✅   |
| Performance analysis                  |    ✅   |

---

## Files Added in Milestone-2

```
src/eval/evaluator.py
src/api/eval_router.py
data/m2_testset_batch1_respond.json
data/m2_testset_batch2_notify.json
data/m2_testset_batch3_ignore.json
results/m2_eval_report.json (auto-generated)
```

---

