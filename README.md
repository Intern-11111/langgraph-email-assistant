# 📧 AI Email Assistant Project — Email Assistant using LangGraph, LangChain & Human-in-the-Loop Architecture


Infosys Springboard Internship Milestone Project

## 📌 Project Title

Intelligent Email Assistant with Human-in-the-Loop using LangGraph and LangChain

## 📌 Submitted By

- Name: Shruthi Meenakshi M
- Program: Infosys Springboard Internship Program
- Track: Generative AI / Agentic AI Systems
- Project Type: Milestone-Based Implementation

## 📌 Project Overview

This project implements an AI-powered Email Assistant system using LangChain and LangGraph frameworks. The system demonstrates:

- Persistent memory handling
- Thread-based conversation management
- Tool execution interruption
- Human approval workflows
- Safe AI execution patterns
- Modular agent pipeline architecture

The assistant simulates real-world enterprise email automation scenarios where human validation is mandatory before sensitive actions such as sending emails.

## 📌 Technologies Used

| Technology       | Purpose                         |
|------------------|---------------------------------|
| Python 3.10+     | Programming Language            |
| LangChain        | LLM orchestration framework     |
| LangGraph        | State-based agent workflow engine |
| MemorySaver      | Conversation checkpointing      |
| Mock Tools       | Email & Calendar simulation     |
| Git              | Version Control                 |
| VS Code          | Development Environment         |

## 📘 Key Concepts Explained

### 🔹 LangChain

LangChain is a framework that simplifies the development of applications powered by Large Language Models (LLMs).

It provides:

- Prompt templates
- Tool calling abstraction
- Memory handling
- Agent workflows
- External API integration

LangChain enables building structured, multi-step AI pipelines rather than single prompt interactions.

### 🔹 LangGraph

LangGraph is a state machine-based extension built on top of LangChain.

It allows developers to:

- Design multi-node workflows
- Control agent execution flow
- Pause and resume execution
- Implement conditional routing
- Maintain state across steps

LangGraph is used to model agent behavior as directed graphs.

### 🔹 LangSmith

LangSmith is an observability and debugging platform for LangChain applications.

It helps developers:

- Track agent execution traces
- Debug prompt chains
- Monitor latency and failures
- Analyze production workflows

LangSmith improves transparency and reliability of AI systems.

### 🔹 MemorySaver

MemorySaver is a LangGraph checkpointing mechanism that:

- Saves intermediate agent states
- Enables session persistence
- Allows recovery after interruptions
- Maintains conversation continuity

### 🔹 Human-in-the-Loop (HITL)

Human-in-the-loop is a safety mechanism where:

- AI pauses before executing sensitive actions
- Human validates or modifies agent decisions
- Execution resumes only after approval

This ensures:

- Compliance
- Ethical AI deployment
- Reduced risk of automated mistakes

## 📂 Folder Structure

```
langgraph-email-assistant/
├── .env
├── .git/
├── .gitignore
├── Environment Setup.md
├── README.md
├── requirements.txt
├── ai/
│   ├── etc/
│   ├── Include/
│   ├── Lib/
│   ├── pyvenv.cfg
│   ├── Scripts/
│   └── share/
├── data/
│   ├── agent_outputs.xlsx
│   ├── cli_mail_inputs.json
│   ├── golden_emails.json
│   ├── test_emails.csv
│   ├── triage_results.xlsx
│   ├── user_contacts.json
│   └── user_events.json
├── Milestone4/
│   ├── agent.py
│   ├── evaluate.py
│   ├── graph.py
│   ├── main.py
│   ├── memory.py
│   ├── tools.py
│   └── README.md
├── src/
│   ├── agents/
│   │   ├── hello_agent.py
│   │   ├── react_loop.py
│   │   ├── simple_agent.py
│   │   └── test_email_agent.py
│   ├── dashboard/
│   │   └── hitl.py
│   ├── evaluation/
│   │   ├── eval/
│   │   │   └── test_email_eval.py
│   │   ├── Metrics/
│   │   │   └── agent_quality_metrics.json
│   │   └── prompt/
│   │       └── prompts.txt
│   ├── milestone1/
│   │   ├── hello.py
│   │   └── sample.py
│   ├── milestone2_eval/
│   │   └── milestone2_eval.py
│   ├── reports/
│   │   ├── approved_actions.json
│   │   ├── escalated_actions.json
│   │   └── Milestone2/
│   │       ├── images/
│   │       └── Milestone2.md
│   ├── tools/
│   │   ├── calendar.py
│   │   ├── contact.py
│   │   ├── get_gmail_refresh_token.py
│   │   └── update_user_events.py
│   ├── triage/
│   │   ├── Importance of triage.md
│   │   ├── Improving method of triage Accuracy.md
│   │   ├── triage_eval.py
│   │   ├── triage_llm.py
│   │   ├── triage_node.py
│   │   └── triage_rules.py
│   ├── utils/
│   │   └── config.py
│   ├── workflow/
│   │   ├── ci.yml
│   │   └── triage_workflow.py
│   ├── ReAct prevents dangerous tool.md
│   ├── ReAct Reasoning Loop & Tooling Lead.md
│   ├── react_loop(demo).py
│   └── react_loop3.py
└── test/
```

## 📁 File Description

### agent.py

Contains agent logic responsible for drafting email content based on user input.

### tools.py

Contains mock tools that simulate:

- Email sending
- Scheduling actions

These tools represent unsafe operations requiring approval.

### graph.py

Defines the LangGraph workflow:

- State definitions
- Node connections
- Agent → Tool execution flow
- Entry and exit points

### memory.py

Implements MemorySaver checkpointing functionality to persist conversation state.

### main.py

Acts as the execution engine:

- Initializes memory and threads
- Executes agent
- Handles human approval
- Updates state
- Runs test cases

## 🏗️ Milestone-wise Implementation

### ✅ Milestone 1 — Agent and Workflow Initialization

#### Objective

To design a basic Email Assistant pipeline with LangGraph.

#### Implemented Features

- Agent creation
- State graph construction
- Workflow routing
- Entry and exit nodes

#### Outcome

Successfully built a modular agent pipeline architecture.

### ✅ Milestone 2 — Memory & Thread Management

#### Objective

To enable session persistence and conversation history tracking.

#### Implemented Features

- MemorySaver integration
- Thread-based configuration
- Checkpoint-based recovery
- Conversation continuity

#### Outcome

Agent maintains state across multiple executions within the same session.

### ✅ Milestone 3 — Human Approval & Interrupt Handling

#### Objective

To prevent unsafe tool execution without human consent.

#### Implemented Features

- Interrupt configuration before tool execution
- Agent pause detection
- State inspection
- Human data correction
- Resume execution mechanism

#### Outcome

System successfully pauses before sending email and resumes only after human validation.

### ✅ Milestone 4 — Integration & Testing

#### Objective

To validate the system with real execution scenarios.

#### Implemented Features

- Mock email and scheduling tools
- Multiple thread sessions
- Rejection handling scenarios
- State update testing
- End-to-end integration

#### Outcome

System passed all test cases and demonstrated stable multi-session behavior.

## ▶️ How To Run The Project

### Step 1 — Install Dependencies

Create virtual environment (optional):

```
python -m venv venv
source venv/bin/activate
```

Install libraries:

```
pip install langchain langgraph openai
```

### Step 2 — Run Application

```
python main.py
```

### Step 3 — Observe Output

You will see:

- Agent execution
- Pause before tool execution
- Human update simulation
- Resume execution
- Email mock sending confirmation

## 🧪 Testing Scenarios Implemented

### Test Case 1 — Normal Approval

- Agent drafts email
- Human approves content
- Email tool executes successfully

### Test Case 2 — Rejection Handling

- Agent generates incorrect email
- Human modifies content
- Updated state resumes execution
- Corrected email sent

## 🔐 Safety Features

This project enforces:

- ✔ Human validation before unsafe actions
- ✔ Controlled execution flow
- ✔ Memory persistence
- ✔ Thread isolation
- ✔ State integrity

## 🎯 Learning Outcomes

Through this project, the following skills were gained:

- Agentic AI system design
- LangGraph workflow modeling
- Stateful AI pipelines
- Human-in-the-loop architecture
- Modular AI engineering
- Enterprise-grade safety patterns

## 📌 Conclusion

This project demonstrates the implementation of a secure, scalable and human-supervised AI Email Assistant using modern agent frameworks. It aligns with real-world enterprise AI deployment standards and showcases best practices in AI safety and workflow orchestration.

## 📎 Future Enhancements

Planned upgrades include:

- Real SMTP email integration
- Calendar API integration
- LangSmith monitoring dashboard
- Role-based approval system
- Web UI dashboard

## ✅ Declaration

I hereby declare that this project is implemented by me as part of the Infosys Springboard Internship Milestone Program and follows academic integrity and project guidelines.