# **Milestone 2**

---

## **1. Introduction**

In Milestone 1, a basic Email Triage Agent was developed using LangGraph to classify incoming emails into three actions: *Respond*, *Ignore*, and *Notify Human*.
Milestone 2 builds upon this foundation by introducing a **Human-in-the-Loop (HITL) interface**, performing **large-scale evaluation**, and using **LangSmith observability** to analyze agent performance and diagnose failures.

---

## **2. Objective of Milestone 2**

The objectives of this milestone are:

* To design a **user interface** that allows human interaction with the email agent.
* To evaluate the agent on a **new dataset of 100+ emails**.
* To verify whether the agent satisfies the defined success criteria.
* To analyze agent failures and identify **root causes** using LangSmith.
* To improve transparency and debuggability of agent decisions.

---

## **3. System Design Overview**

The Milestone 2 system consists of:

* A **Streamlit-based UI** for manual email input.
* The **Milestone 1 email triage agent** integrated into the UI.
* A **batch evaluation pipeline** for testing multiple emails(100+ emails).
* **LangSmith dashboard** for monitoring, tracing, and analysis.

The UI acts as the Human-in-the-Loop layer, enabling humans to observe and validate agent behavior.

---

## **4. Human-in-the-Loop (HITL) UI Implementation**

A Streamlit application was developed to serve as the HITL interface.

### **UI Features**

* Text area for entering email content manually.
* Button to execute the email triage agent.
* Visual display of the agent’s decision.

### **Possible Agent Decisions**

* **Respond** – The email requires a reply.
* **Ignore** – The email does not require action.
* **Notify Human** – The email requires immediate human intervention.

This UI allows easy testing, demonstration, and validation of agent behavior.

---

## **5. Large-Scale Evaluation on New Email Dataset**

The agent was evaluated using **100+ email samples** provided by another intern.

### **Evaluation Process**

* Each email was passed through the Milestone 1 agent.
* The predicted action was recorded.
* Outputs were compared against expected behavior.

### **Success Criteria**

* Agent must produce a valid action for every email.
* Output must be one of: *Respond*, *Ignore*, or *Notify Human*.
* No execution failures during batch evaluation.
* Consistent behavior across similar email patterns.

---

## **6. LangSmith Observability & Performance Analysis**

LangSmith was used to:

* Track individual agent executions.
* Observe decision patterns across the dataset.
* Measure overall agent accuracy.
* Identify anomalous or inconsistent decisions.

The dashboard provided detailed traces that helped understand how the agent reached specific decisions.

---

## **7. Failure Case Analysis and Root Cause Diagnosis**

### **Failure Case 1: Over-triggering Human Notification**

**Email Example:**
“Please do the needful at the earliest.”

**Agent Output:** Notify Human
**Expected Output:** Respond

**Root Cause:**
The agent relies heavily on urgency-related keywords without sufficient context evaluation.

---

### **Failure Case 2: Short Critical Emails**

**Email Example:**
“System down. Immediate fix required.”

**Agent Output:** Ignore
**Expected Output:** Notify Human

**Root Cause:**
Length-based filtering caused important short emails to be misclassified.

---

### **Failure Case 3: Polite Requests**

**Email Example:**
“Kindly review the attached document when convenient.”

**Agent Output:** Ignore
**Expected Output:** Respond

**Root Cause:**
Polite language lacked explicit urgency or action keywords, leading to under-prioritization.

---

## **8. Key Learnings from Milestone 2**

* HITL interfaces significantly improve agent transparency.
* Keyword-based logic is insufficient for nuanced email classification.
* Observability tools like LangSmith are essential for diagnosing failures.
* Real-world datasets expose edge cases not visible in small test sets.

---

## **9. Conclusion**

Milestone 2 successfully extended the Email Assistant agent by introducing a Human-in-the-Loop UI, conducting large-scale evaluation, and performing detailed failure analysis using LangSmith.
This milestone established a strong foundation for further improvements in agent reasoning, accuracy, and robustness.

---

## **10. Future Scope**

* Incorporate semantic understanding using advanced LLM prompts.
* Add confidence scores to agent decisions.
* Improve handling of short but critical emails.
* Introduce feedback-based learning to refine agent behavior.

