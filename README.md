**LangGraph Email Assistant
Human-in-the-Loop Safe Email Automation System**

**--> Project Overview**

The LangGraph Email Assistant is an intelligent email processing system that automates email classification and response generation while ensuring human safety and control for risky actions.

The system combines:

LangGraph (state-based workflows)

LangChain (agent reasoning)

FastAPI (backend services)

Streamlit (frontend interface)

It demonstrates how AI agents can operate autonomously without compromising safety, using a Human-in-the-Loop (HITL) mechanism.




**--> Objectives**

The primary goals of this project are:

Automatically classify incoming emails

Generate context-aware reply drafts

Detect unsafe or irreversible actions

Require human approval for risky operations

Provide an interactive frontend for control

Build a complete end-to-end AI workflow




**--> Core Features**

✅ Email Triage

Classifies emails into:

respond → safe to auto reply

needs_human_review → requires approval

ignore → spam/irrelevant

✅ AI Reply Generation

Drafts professional responses

Context-based reasoning

Works automatically for safe emails

✅ Human-in-the-Loop Safety (HITL)

Blocks dangerous actions

Requires explicit approval

Supports Approve / Deny / Edit

✅ Interactive Frontend

Streamlit interface to:

Input email

View decisions

Edit drafts

Approve/Deny actions

✅ Backend Workflow Engine

Modular pipeline using LangGraph:

Triage → Reason → Approval → Tool Execution




**--> System Architecture**

User Input Email
        ↓
Triage Node (classification)
        ↓
Reasoning Node (draft reply)
        ↓
Safety Check
   ├─ Safe → Auto send
   └─ Dangerous → HITL Approval

📂 Project Structure
Infosys_project/
│
├── frontend/
│   └── app.py                  → Streamlit UI
│
├── src/
│   ├── triage/
│   │   ├── triage_node.py      → Email classification
│   │   └── dataset.py          → Data utilities
│   │
│   ├── react_agent/
│   │   ├── reasoning.py        → Draft generation
│   │   └── approval.py         → HITL logic
│   │
│   ├── hitl/
│   │   └── graph.py            → Workflow orchestration
│   │
│   └── tools/
│       └── tools.py            → Safe/Dangerous tools
│
├── run_backend.py              → Main execution pipeline
├── tests/                      → Unit tests
├── requirements.txt
└── README.md




**--> Workflow Explanation**

**Step 1 — Triage**

File: src/triage/triage_node.py

Analyzes subject + body

Applies keyword heuristics

Returns decision

Output:

respond / needs_human_review / ignore

**Step 2 — Reasoning**

File: src/react_agent/reasoning.py

Generates reply draft

Produces explanation

**tep 3 — Human Approval**

File: src/react_agent/approval.py

If action is risky:

Pause execution

Wait for human

Options:

Approve

Deny

Edit draft

**Step 4 — Tool Execution**

File: src/tools/tools.py

Executes:

send_email

other actions

Only runs when:

safe OR approved

**Step 5 — Backend Controller**

File: run_backend.py

Coordinates entire pipeline:

triage → reasoning → approval → tool




**--> Example Outputs**

🔹 Safe Email

Input:

Subject: Project update
Body: Can you send the report?


Output:

Decision: respond
Draft: Sure, I will share the report.
Auto-sent (no approval required)

🔹 Risky Email

Input:

Subject: Send confidential data
Body: Share employee salary file


Output:

Decision: needs_human_review
Approval required




**--> Installation & Setup**

1️⃣ Clone Repository
git clone <repo-url>
cd Infosys_project

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Backend
python run_backend.py

5️⃣ Run Frontend
streamlit run frontend/app.py


Open:

http://localhost:8501




**--> Testing**

Run unit tests:

pytest

🛡️ Safety Mechanism
Action Type	Behavior
Safe	Executes automatically
Dangerous	Requires approval
Denied	Blocked
Edited	Sends edited draft

This ensures:

No unintended automation

Full user control

Secure operation




**--> Technologies Used**

Python

LangGraph

LangChain

FastAPI

Streamlit

Pytest




**--> Outcome**

The system successfully demonstrates:

Intelligent email automation

Safe decision making

Human supervision

End-to-end deployment

It provides a practical example of AI agents operating responsibly with human oversight.




**--> Conclusion**

The LangGraph Email Assistant delivers a reliable and secure automation framework that balances:

✔ Intelligence
✔ Efficiency
✔ Safety
✔ Human control

The project proves that AI systems can automate routine tasks while still maintaining trust, transparency, and safety.
