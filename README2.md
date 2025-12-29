## 📌 Milestone 2: Human-in-the-Loop (HITL) UI + Evaluation & Analysis

---

## 🎯 Goal of Milestone 2

The goal of **Milestone 2** is to extend the Milestone 1 email triage agent by:

1. Building a **Human-in-the-Loop (HITL) User Interface** using **Streamlit**
2. Running the **Milestone 1 agent** on a **new dataset of 100+ emails** provided by Intern 1
3. Verifying whether the agent meets the **success criteria** across all test cases
4. Tracking executions and accuracy using **LangSmith Observability Dashboard**
5. Analyzing failed cases and **diagnosing root causes** for incorrect agent decisions

---

## ✅ What Was Done in Milestone 2

### 1️⃣ Streamlit-Based UI Development

A web-based UI was built using **Streamlit** to allow manual testing and demonstration of the agent.

#### UI Features:

* Text area to **manually input email content**
* Button to trigger the agent execution
* Displays agent decision as one of:

  * `respond`
  * `ignore`
  * `notify_human`
* Clear visual feedback using color-coded status messages

This UI enables **Human-in-the-Loop validation**, making it easy for mentors or evaluators to understand how the agent behaves.

---

### 2️⃣ Agent Execution on 100+ Emails

* Used the **Milestone 1 email triage agent** logic
* Ran the agent against **100+ new email examples** provided by Intern 1
* Verified outputs against expected behavior
* Categorized decisions into:

  * Correct
  * Incorrect

---

### 3️⃣ Success Criteria Verification

The success criteria checked:

* Can the agent **successfully score all test cases**?
* Does it correctly identify:

  * Short / low-value emails → `ignore`
  * Normal emails → `respond`
  * Risky / urgent emails → `notify_human`

All test cases were processed without runtime failures.

---

### 4️⃣ LangSmith Observability & Accuracy Tracking

* Integrated the agent with **LangSmith**
* Tracked:

  * Execution traces
  * Input–output mappings
  * Decision distributions
* Calculated overall accuracy across the dataset

LangSmith helped identify **patterns in failures** and decision bias.

---

### 5️⃣ Failure Analysis & Root Cause Diagnosis

#### Example Failure Cases:

| Email Content                           | Expected     | Agent Output | Root Cause                            |
| --------------------------------------- | ------------ | ------------ | ------------------------------------- |
| "Please do the needful at the earliest" | notify_human | respond      | Phrase not explicitly marked as risky |
| Very short but urgent email             | notify_human | ignore       | Length-based rule overpowered urgency |
| Polite escalation without keywords      | notify_human | respond      | Keyword-based detection limitation    |

#### Diagnosed Root Causes:

* Over-reliance on **keyword matching**
* Simple **length-based heuristics** caused misclassification
* Lack of semantic understanding (no LLM reasoning yet)

These insights will guide improvements in future milestones.

---

## 🖥️ How to Run the UI

```bash
# Activate virtual environment
venv\Scripts\activate

# Run Streamlit app
streamlit run app.py
```

The UI opens in the browser at:

```
http://localhost:8501
```

---

## 📂 Project Structure

```
langgraph-email-assistant/
│
├── app.py                 # Streamlit UI (Milestone 2)
├── README.md              # Project documentation
├── requirements.txt       # Dependencies
├── .env                   # API keys (not committed)
│
├── src/
│   ├── agent.py           # Email triage agent logic
│   ├── hello_agent.py     # Milestone 1 environment check
│   ├── triage_agent.py    # Agent orchestration
│   ├── run_eval.py        # Batch evaluation on 100+ emails
│   ├── golden_emails.py   # Test email dataset
│   └── __init__.py
│
├── docs/
│   └── ENV_SETUP.md       # Environment setup guide
│
└── venv/                  # Virtual environment
```

---

## 📌 Summary

* Successfully built a **Streamlit-based HITL UI**
* Evaluated the agent on **100+ real-world email examples**
* Verified success criteria and execution stability
* Used **LangSmith** for observability and accuracy analysis
* Identified clear **failure patterns and root causes**

Milestone 2 lays a strong foundation for improving agent intelligence and safety in upcoming milestones.

---

✅ **Milestone 2 Completed Successfully**
