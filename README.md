# Ambient Email Agent using LangGraph - langgraph-email-assistant
"Building an Ambient Agent with LangGraph for an Email Assistant"
Milestone 1: Core Email Triage Agent
Overview:

Milestone 1 focuses on building the foundation of the email assistant. The objective is to automatically understand incoming email content and decide what action should be taken. This milestone introduces the use of LangGraph’s StateGraph to structure the decision-making process in a clear and maintainable way.

Functionality:

In this stage, the agent receives an email as input and classifies it into one of three categories:

ignore – promotional or low-priority emails that do not require action

respond – emails that require a reply, such as meeting requests

notify_human – sensitive or important emails that require human attention

The classification logic is implemented using simple intent-based rules and keyword checks. Each decision is accompanied by a short reasoning, making the agent’s behavior transparent.

Technical Implementation:

LangGraph’s StateGraph is used to define the workflow. The graph starts with an email input state, passes it through the triage node, and outputs the decision along with reasoning. This milestone establishes a clean modular structure that allows future extensions.

Outcome:

By the end of Milestone 1, the system can reliably understand email intent and route emails correctly. This milestone serves as the core decision engine for the entire project.

Milestone 2: Evaluation and Accuracy Measurement
Overview:
Milestone 2 introduces quantitative evaluation to measure how well the email triage agent performs. Instead of relying only on manual testing, this milestone focuses on validating the system using a structured dataset.

Functionality:

A dataset of 100 realistic emails is created, where each email is labeled with the expected action (ignore, respond, or notify_human). The evaluation script automatically runs the triage agent on each email and compares the predicted decision with the expected label.

Technical Implementation:

The evaluation module:

Loads the dataset from a JSON file
Invokes the LangGraph triage agent for each email
Counts correct prediction
Calculates overall accuracy

This provides a clear numerical metric to understand the system’s performance.

Outcome

Milestone 2 produces measurable results such as total emails tested, correct predictions, and accuracy percentage. This milestone helps identify strengths and limitations of the triage logic and prepares the system for improvement through human feedback.

Milestone 3: Human-in-the-Loop (HITL) Interaction
Overview

Milestone 3 introduces human control and safety into the system. The goal is to ensure that the agent does not operate fully autonomously in critical situations and can learn from human decisions.

Functionality:

A Pause State is added to the LangGraph workflow. When the agent makes a decision, execution pauses and waits for human input. Depending on the situation, the human can:

Approve the agent’s decision
Deny the action
Edit the response
For example, if the agent suggests replying to an email, a human can edit the response to correct or refine it.

Learning Aspect:

When a human edits a response, the correction is stored in memory. If a similar email appears in the future, the agent automatically reuses the stored preference without asking again. This introduces a basic learning mechanism based on human feedback.

Outcome:

By the end of Milestone 3, the system becomes interactive, safer, and adaptive. It demonstrates true Human-in-the-Loop behavior, where humans guide and improve the agent over time.

 Milestone 4: Tool Interrupts and Safe Execution
Overview:

Milestone 4 focuses on preventing unsafe or irreversible actions. The goal is to ensure that sensitive tools (such as sending an email) are never executed without explicit human approval.

Functionality:

Certain actions are flagged as unsafe tools, such as send_email. The LangGraph workflow is configured using:

interrupt_before = ["tools"]
This causes the graph to pause just before a tool is executed.

Human Approval:

When the interrupt occurs:
The system clearly notifies the user
The human is asked to approve or deny the tool execution
The tool runs only if approval is granted

If denied, the action is safely blocked.

Outcome:

Milestone 4 guarantees strong safety and control. No sensitive operation can occur without human consent. This makes the system suitable for real-world deployment scenarios.