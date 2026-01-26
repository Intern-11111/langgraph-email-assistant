# Team Contributions Summary - Group A1

**Project:** Building an Ambient Agent with LangGraph for an Email Assistant  
**Team:** Group A1  
**Members:** 4 Interns

---

## 👨‍💻 Aayush J Shah - Environment & Infrastructure Lead

### Milestone 1: Environment & Infrastructure Setup
**Focus:** Development setup, tooling, dependency management, repo collaboration

**Responsibilities:**
- Set up the complete development environment
- Configure project dependencies and `requirements.txt`
- Establish repository collaboration workflows
- Configure LLM integrations (Gemini, Hugging Face)
- Set up `.env` configuration and API key management
- Create initial project structure

---

### Milestone 2: Test Dataset Creation
**Focus:** Work on creation of test dataset: 100+ high quality examples, draft the varied incoming email scenarios, write ideal outcome or perfect reply for each (the ground truth), Format the data (CSV/JSON) for testing the framework

**Responsibilities:**
- Create comprehensive test dataset with 100+ email examples
- Draft varied email scenarios:
  - Meeting requests
  - Spam/promotional emails
  - Urgent queries
  - Information requests
  - Calendar invites
  - Approval requests
- Write ideal/ground truth responses for each email
- Format dataset in both CSV and JSON formats
- Ensure balanced representation across triage categories

---

### Milestone 3: Dangerous Tools Identification
**Focus:** Identify "dangerous" tools, "Undo Test", Tag your dangerous tools

**Responsibilities:**
1. **Identify "dangerous" tools** (e.g., `send_email`, `create_calendar_invite`)
2. **"Undo Test"**: The rule is—changes reality (sends email, moves money, deletes files), it is Dangerous. If it just looks at data (checks weather, reads files), it is Safe
3. **Tag your dangerous tools** so that agent knows to stop

---

### Milestone 4: Safety Mechanisms & Interrupts
**Focus:** Flag Unsafe Tools, Configure Interrupts, Notify User, Deliverable

**Responsibilities:**
1. **Flag Unsafe Tools:** Identify sensitive actions (e.g., `send_email`) requiring approval
2. **Configure Interrupts:** Set `interrupt_before=["tools"]` during graph compilation to pause execution
3. **Notify User:** Print a clear alert when the agent pauses
4. **Deliverable:** The agent successfully pauses before execution to await human input

---

## 👨‍💻 Ganesh Sai Manideep Bandaru - Triage Node & Dataset Lead

### Milestone 1: Triage Node & Dataset
**Focus:** Core ML logic for classification + evaluation dataset

**Responsibilities:**
- Build the triage node for email classification
- Implement 3-class classifier (ignore, notify-human, respond-act)
- Create balanced golden dataset (48 emails)
- Fine-tune transformer model (DistilBERT)
- Combine rule-based logic with ML predictions
- Achieve robust classification accuracy
- Create evaluation dataset for testing

---

### Milestone 2: Quality Metrics Definition
**Focus:** Define metrics for the 'Agent Quality Score', Formulate specific questions for the Judge LLM, Define the scoring rubric (Binary Pass/Fail vs. 1-5 Scale)

**Responsibilities:**
- Define quality metrics: **Helpfulness**, **Tone**, **Accuracy**
- Formulate specific evaluation questions for the Judge LLM
- Design scoring rubric:
  - 1-5 Scale for each metric
  - Binary Pass/Fail (overall score ≥4 = PASS)
- Create structured evaluation criteria
- Implement Pydantic models for judge scoring

---

### Milestone 3: HITL Checkpoint & State Persistence
**Focus:** Modify the agent's graph to add a HITL Checkpoint, Concept: Saving the Game, Rule: You must save the agent's state (memory) to a database so it can pause without forgetting everything, Action: Use `interrupt_before=["action_node"]` in your graph code

**Responsibilities:**
1. **Modify the agent's graph** to add a HITL Checkpoint
2. **Concept: Saving the Game** - Implement state persistence
3. **Rule:** Save the agent's state (memory) to a database so it can pause without forgetting everything
4. **Action:** Use `interrupt_before=["action_node"]` in graph code

---

### Milestone 4: Memory Persistence System
**Focus:** Implement MemorySaver, Manage Thread IDs, Compile the graph with checkpointer=memory, Ensure history survives within the session

**Responsibilities:**
1. **Implement MemorySaver** - Set up persistent memory system
2. **Manage Thread IDs** - Track conversation threads
3. **Compile the graph with `checkpointer=memory`**
4. **Ensure history survives within the session** - State persists across restarts

---

## 👩‍💻 Samruddhi Maslage - ReAct Reasoning Loop & Tooling Lead

### Milestone 1: ReAct Reasoning Loop & Tooling
**Focus:** Build agent brain + mock actions

**Responsibilities:**
- Build the ReAct (Reason + Act) reasoning loop
- Implement the "thinking" cycle: Reason → Act → Observe
- Create mock tools for safe development:
  - `read_calendar` - Returns mock calendar events
  - `lookup_contact` - Returns mock contact information
- Design tool calling logic
- Implement safe tool execution without real-world effects

---

### Milestone 2: LLM-as-a-Judge Evaluation System
**Focus:** "Set up the 'LLM-as-a-judge' evaluator within LangSmith using Python, Configure LangSmith to accept the dataset from the CSV/JSON extraction, Implement custom evaluators based on the criteria, Ensure the system automatically scores responses."

**Responsibilities:**
- Set up LLM-as-a-judge evaluator within LangSmith using Python
- Configure LangSmith to accept dataset from CSV/JSON
- Implement custom evaluators based on quality criteria
- Ensure automatic scoring of agent responses
- Create evaluation pipeline for batch testing
- Integrate with LangSmith dashboard for trace visualization

---

### Milestone 3: Testing & Tracing Framework
**Focus:** Connect Langsmith for tracing, safety tests, Design a Test Cases for Safe and Dangerous, Write a test code whether the pause triggers or not, identify the waited input was successfully or not, Final Report

**Responsibilities:**
1. **Connect Langsmith** for tracing and safety tests
2. **Design Test Cases** for Safe and Dangerous actions
3. **Write a test code** whether the pause triggers or not, identify if the waited input was successful or not
4. **Final Report** documenting all test results

---

### Milestone 4: State Management & Resume Logic
**Focus:** Inspect State, Update State, Resume Logic, Deliverable

**Responsibilities:**
1. **Inspect State:** Use `graph.get_state` to review pending actions
2. **Update State:** Implement `update_state` to modify agent drafts (e.g., correcting names)
3. **Resume Logic:** Ensure the graph resumes with the new information
4. **Deliverable:** A script demonstrating the agent's draft being changed before tool execution

---

## 👩‍💻 Payal Kokane - HITL + UI & LangSmith Observability Lead

### Milestone 1: HITL + UI & Observability
**Focus:** Human safety + debugging visibility

**Responsibilities:**
- Design Human-in-the-Loop (HITL) workflow
- Create HITL dashboard for user approval
- Implement Approve/Edit/Deny controls
- Build debugging visibility features
- Ensure no dangerous actions execute without approval
- Create decision tracking system (decisions.json)

---

### Milestone 2: Agent Evaluation & Analysis
**Focus:** Run the Milestone 1 agent against the new 100+ example dataset, Verify the success rate: Can the framework successfully score all test cases?, Analyze where the agent failed, Diagnose the root cause

**Responsibilities:**
- Run Milestone 1 agent against 100+ example dataset
- Verify success rate: Can the framework successfully score all test cases?
- Analyze where the agent failed
- Diagnose the root cause of failures
- Create comprehensive evaluation report
- Document failure patterns and improvement recommendations

---

### Milestone 3: Testing & Validation
**Focus:** Connect Langsmith for tracing, safety tests, Design a Test Cases for Safe and Dangerous, Write a test code whether the pause triggers or not, identify the waited input was successfully or not, Final Report

**Responsibilities:**
1. **Connect Langsmith** for tracing and safety tests
2. **Design Test Cases** for Safe and Dangerous actions
3. **Write test code** to verify pause triggers and human input validation
4. **Final Report** with comprehensive test documentation

---

### Milestone 4: Integration & Final Assembly
**Focus:** Integration & Testing: Create Mock Tools, Test Edge Cases, Assemble Script, Deliverable

**Responsibilities:**
1. **Integration & Testing:** Bring all components together
2. **Create Mock Tools:** Build dummy functions for email and scheduling
3. **Test Edge Cases:** Verify handling of user rejections and interruptions
4. **Assemble Script:** Combine code from Members 1-3 into `main.py`
5. **Deliverable:** Final submission script and a test case log

---

## Summary Matrix

| Milestone | Aayush Shah | Ganesh Bandaru | Samruddhi Maslage | Payal Kokane |
|-----------|-------------|----------------|-------------------|--------------|
| **M1** | Environment & Infrastructure | Triage Node & Dataset | ReAct Loop & Tools | HITL Workflow & UI |
| **M2** | Test Dataset (100+) | Quality Metrics | LLM-as-a-Judge | Agent Evaluation |
| **M3** | Dangerous Tools | State Persistence | Testing Framework | Pause Validation |
| **M4** | Safety Interrupts | MemorySaver | State Management | Final Integration |

---

## Key Deliverables by Team

### Development Infrastructure
- **Lead:** Aayush Shah
- Environment setup, dependencies, test datasets

### Core Agent Intelligence
- **Lead:** Ganesh Bandaru
- Triage classification, quality metrics, memory system

### Reasoning & Tools
- **Lead:** Samruddhi Maslage
- ReAct loop, mock tools, evaluation framework

### Safety & Integration
- **Lead:** Payal Kokane
- HITL controls, testing, final assembly

---

## Individual Documentation

For detailed technical contributions and code examples, refer to individual README files:

- 📄 [Aayush Shah - Detailed Contributions](../AayushShah/README.md)
- 📄 [Ganesh Sai Manideep Bandaru - Detailed Contributions](../Ganesh_Sai_Manideep_Bandaru/README.md)
- 📄 [Samruddhi Maslage - Detailed Contributions](../SamruddhiMaslage/README.md)
- 📄 [Payal Kokane - Detailed Contributions](../Payal_Kokane/README.md)

---

## Project Resources

- 📘 [Complete Project README](README.md)
- 📗 [Project Setup Guide](PROJECT_SETUP.md)
- 📕 [Final Project Report](FINAL_REPORT.md)

---

**Document Version:** 1.0  
**Last Updated:** January 26, 2026  
**Source:** Official Task Allocation Spreadsheet (Batch1-Email Assistant Group A1.xlsx)
