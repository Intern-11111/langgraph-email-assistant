# 🚀 LangGraph Email Assistant  
### *Building an Ambient Agent with LangGraph for Intelligent Email Automation*

An **intelligent ambient agent** built using **LangGraph** to process, analyze, and automate email workflows with **real-time assistance** and **proactive AI-driven insights**.

---

## 🚀 Project Overview

This project focuses on building an **AI-driven email assistant** using **LangGraph**, enabling structured agent workflows, intelligent decision-making, and seamless LLM integration.

The system is designed to evolve into a full-fledged ambient agent capable of:

* Email triage
* Context-aware analysis
* Automated responses
* Proactive assistance

---

## 🎯 Milestone 1 Goal

The objective of **Milestone 1** was to establish a strong technical foundation by:

* Setting up the development environment
* Defining a scalable project structure
* Validating core AI frameworks
* Implementing an initial **HelloAgent** using LangGraph
* Demonstrating end-to-end system functionality

---

## ✅ What Was Accomplished in Milestone 1

### 🔧 Environment & Infrastructure (Lead Responsibility)

* Created and validated a **Python virtual environment**
* Installed and locked all required dependencies
* Configured `.gitignore` to exclude:

  * `venv/`
  * `.env`
  * cache and build files
* Secured API configuration using `.env` for **Gemini API Key**
* Structured the repository for scalability and future expansion

---

### 🔐 API Configuration

* Integrated **Google Gemini** using `langchain-google-genai`
* API key securely managed using environment variables:

  ```
  GOOGLE_API_KEY=your_api_key_here
  ```

---

### 📦 Dependency Validation

The following libraries were installed and validated successfully:

* `langchain`
* `langgraph`
* `langchain-google-genai`
* `transformers`
* `datasets`
* `fastapi`
* `uvicorn`

All dependencies were tested to ensure compatibility and stability.

---

### 🤖 Core Functionality – HelloAgent

* Implemented **HelloAgent**, a foundational LangGraph-based agent
* Powered by **Gemini LLM**
* Validated:

  * Graph state execution
  * LLM connectivity
  * Successful API handshakes with Google Gemini
* Served as a **proof-of-concept** and foundation for future triage and automation logic

---

## 🗂️ Project Structure

```text
langgraph-email-assistant/
├── src/                     # Core application and agent logic
│   ├── agents/              # Agent implementations (hello_agent.py, triage logic)
├── run_server.py            # FastAPI server entry point
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── env_setup.md             # Environment setup guide
└── .gitignore               # Ignore venv, .env, cache files
```

---

## ▶️ Running the Project

### 1️⃣ Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure environment variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

### 4️⃣ Run the server

```bash
python run_server.py
```

---

## 🔮 Future Enhancements

* Advanced email triage and classification
* Multi-agent orchestration using LangGraph
* Context-aware response generation
* Integration with real email providers (Gmail/Outlook)
* Proactive notifications and insights

---

## 📌 Tech Stack

* **Python**
* **LangGraph**
* **LangChain**
* **Google Gemini**
* **FastAPI**
* **Uvicorn**

---

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

✅ **Milestone 2 Completed Successfully**<hr>

# 🛑 Milestone 3  
## Human-in-the-Loop (HITL) Safety with LangGraph & LangSmith

---

## 1. Introduction

As AI agents become increasingly autonomous, it is critical to ensure that **unsafe or irreversible actions are never executed without human oversight**.

Milestone 3 focuses on implementing a **Human-in-the-Loop (HITL) safety mechanism** for an AI-based Email Assistant.  
This milestone ensures that **risky email actions trigger a pause**, allowing a human to review and approve before execution.

This implementation uses:


- **LangGraph** for workflow orchestration  
- **LangSmith** for tracing, observability, and safety validation  

---

## 2. Objectives of Milestone 3

The primary goals of this milestone are:

- Integrate LangSmith for tracing and observability
- Design and validate safe and dangerous test cases
- Implement pause (interrupt) logic for risky actions
- Verify that execution waits for human input
- Ensure safe resumption or termination of execution
- Document and report safety behavior clearly

---

## 3. System Architecture Overview

The system is composed of the following components:

- **LangGraph** – Defines the agent workflow using a state graph
- **Triage Agent** – Classifies incoming emails
- **HITL Interrupt Node** – Pauses execution for dangerous actions
- **Human Approval Logic** – Approves, denies, or edits actions
- **LangSmith** – Tracks all executions and decisions

---

## 4. High-Level Workflow

1. Email content is received as input
2. The email is classified as:
   - `respond`
   - `ignore`
   - `notify_human`
3. Safe actions (`respond`, `ignore`) proceed automatically
4. Dangerous actions (`notify_human`) trigger an interrupt
5. The agent pauses and waits for human input
6. Based on human decision:
   - Approved → execution resumes
   - Denied → execution terminates safely

---

## 5. LangSmith Integration

LangSmith was enabled using environment variables:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=langgraph-email-assistant
LANGCHAIN_API_KEY=****
````

### Benefits of LangSmith

* Full execution trace visibility
* Validation of safe vs dangerous routing
* Clear confirmation of pause and resume behavior
* Easier debugging and safety auditing

All agent executions appear under the **langgraph-email-assistant** project in the LangSmith dashboard.

---

## 6. Test Case Design

To validate HITL behavior, multiple test cases were designed.

### 6.1 Safe Email Test Cases

| Test Case | Email Content                       | Expected Behavior     |
| --------- | ----------------------------------- | --------------------- |
| Safe-1    | Schedule a meeting                  | Respond automatically |
| Safe-2    | Thanks for the update               | Ignore                |
| Safe-3    | Please review the attached document | Respond automatically |

Safe emails **do not trigger a pause** and complete execution normally.

---

### 6.2 Dangerous Email Test Cases

| Test Case | Email Content                         | Expected Behavior      |
| --------- | ------------------------------------- | ---------------------- |
| Danger-1  | Delete all production data            | Pause + Human approval |
| Danger-2  | Send money urgently to this account   | Pause + Human approval |
| Danger-3  | Reset all admin passwords immediately | Pause + Human approval |

Dangerous emails **trigger an interrupt and wait for human input**.

---

## 7. HITL Pause and Resume Validation

* Dangerous emails invoke the `interrupt()` node
* Execution pauses and does not proceed automatically
* The system waits for explicit human input (`approved = True / False`)
* Safe emails bypass HITL logic entirely
* Execution resumes only after human approval

This confirms that **HITL safety is correctly enforced**.

---

## 8. Results and Observations

From LangSmith dashboard analysis:

* All dangerous emails correctly triggered `notify_human`
* All safe emails completed without interruption
* Each test case generated a distinct trace
* Execution latency remained within acceptable limits
* Pause and resume behavior was clearly visible in traces

---

## 9. Key Learnings

* Human-in-the-Loop is essential for safe AI systems
* LangGraph interrupts provide clean pause–resume control
* LangSmith greatly simplifies debugging and safety validation
* Multiple test cases increase confidence in agent reliability

---

## 10. Conclusion

Milestone 3 successfully implements a **robust Human-in-the-Loop safety mechanism**.

The system ensures that:

* High-risk actions are never executed autonomously
* Safe actions remain fast and efficient
* Human oversight is enforced only when necessary

This milestone demonstrates:

* Responsible AI design
* Production-ready safety controls
* Strong observability and validation using LangSmith

---

✅ **Milestone 3 Completed Successfully**<hr>

# Milestone 4 – Integration & Testing  

---

## 📌 Objective

The objective of **Milestone 4** is to integrate all previously developed components of the LangGraph-based Email Assistant and validate the system through testing. This milestone focuses on **mock tool integration**, **edge-case handling**, **Human-in-the-Loop (HITL) stability**, and **final deliverables**.

---

## ✅ Tasks Completed

### 1. Create Mock Tools
Dummy tools were implemented to safely simulate real-world actions without using external APIs.

**Implemented Mock Tools:**
- `mock_send_email()` – Simulates sending an email
- `mock_ignore_email()` – Simulates ignoring an email
- `mock_sensitive_action()` – Simulates a risky action requiring human approval
- `mock_deny_action()` – Simulates human rejection of an action

📂 File: `src/mock_tools.py`

---

### 2. Test Edge Cases
Edge cases were tested to ensure system robustness and prevent runtime failures.

**Edge Cases Tested:**
- Empty email input
- Ambiguous email input (e.g., vague requests)

The LangGraph routing logic was hardened to ensure that only valid decisions (`respond`, `ignore`, `notify_human`) are used during graph transitions.

📂 File: `tests/test_edge_cases.py`

**Sample Output:**
```

✅ Empty email handled safely: {'email_body': '', 'decision': 'ignore'}
✅ Ambiguous email handled safely: {'email_body': 'Please do the needful', 'decision': 'respond'}

````

### 3. Assemble Final Script
All components developed in previous milestones were integrated into a single execution script.

**Integrated Components:**
- Triage decision logic
- Human-in-the-Loop (HITL) approval mechanism
- Mock tool execution
- Logging of outcomes

📂 File: `main.py`

---

### 4. Final Deliverables
The following deliverables were generated as part of this milestone:

- ✅ Final runnable script (`main.py`)
- ✅ Edge-case test script (`test_edge_cases.py`)
- ✅ Execution log file (`test_case_log.txt`)

The log file captures decisions, approvals, rejections, and execution timestamps.

---

## 🧠 Key Design Considerations

- **Safe Defaults:** Invalid or unexpected LLM outputs are sanitized before graph routing.
- **HITL Safety:** Risky actions pause execution until human approval is received.
- **Robustness:** The system does not crash for empty or ambiguous inputs.
- **Modularity:** Mock tools are used to ensure safe testing and easy future deployment.

---

## ▶️ How to Run

### Activate Virtual Environment
```powershell
venv\Scripts\activate
````

### Run Edge Case Tests

```powershell
python tests/test_edge_cases.py
```

### Run Main Application

```powershell
python main.py
```

---


## ✅ Conclusion

Milestone 4 successfully integrates all components of the LangGraph Email Assistant and validates system stability through testing. The application is now robust, HITL-safe, and ready for further extension with persistent memory and real-world APIs.

---

✅ **Milestone 4 Completed Successfully**<hr>
