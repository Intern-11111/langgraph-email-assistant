**Milestone 1 – Triage Node & Dataset**

1. Task Description

The task of Milestone 1 is to implement an email triage module that automatically classifies incoming emails into predefined categories so that the email assistant can decide the next action.



2. Implementation

A labeled email dataset was created with categories such as:

reply_immediately

needs_human_review

ignore

spam

Email subject and body are combined and preprocessed using basic text cleaning.

TF-IDF vectorization is used to convert text into numerical features.

A Logistic Regression model is trained to classify emails.

The prediction logic is wrapped inside a triage node function, making it compatible with a LangGraph workflow.



3. Execution Process

Dataset is loaded and split into training and testing sets.

The model is trained on the training data.

Model performance is evaluated using accuracy and classification report.

A sample email is passed to the triage node.

The node outputs a triage decision.



4. Purpose / Usage

This milestone is used to:

Automatically analyze incoming emails

Decide how each email should be handled

Reduce manual email review

Act as the decision-making component of the ambient email agent




5. Output Explanation

The output includes:

Classification accuracy and evaluation metrics

A triage decision for the given email

Sample Output
triage_decision: needs_human_review


This output is passed to the next agent node for further action.



6. Files Used 
File Name-------	Purpose
dataset.py-------	Loads and preprocesses email data
model.py---------	Trains the classification model
evaluate.py------	Evaluates model performance
triage_node.py-----	Generates triage decision
run_triage.py------	Executes Milestone 1


7. How to Execute 
python run_triage.py


---------------------------------------------------------------------------------------------

**Milestone 2 – Agent Quality Score Evaluation
**

1. Task Description

The task of Milestone 2 is to design a quality evaluation framework to measure how well the email assistant’s responses perform from a human perspective.




2. Implementation

Three evaluation metrics were defined:

Helpfulness

Accuracy

Tone

Structured evaluation questions were designed for a Judge LLM.

A 1–5 scoring scale was used for each metric.

A final Agent Quality Score is calculated as the average of all metric scores.




3. Execution Process

The agent response is evaluated using predefined quality metrics.

Each metric receives a score between 1 and 5.

The scores are averaged to compute the final Agent Quality Score.

The final quality score is displayed.




4. Purpose / Usage

This milestone is used to:

Evaluate the quality of agent responses

Ensure responses are helpful, accurate, and well-toned

Provide a measurable quality benchmark

Improve agent behavior over time




5. Output Explanation

The output includes:

Individual metric scores

Final Agent Quality Score

Sample Output
Helpfulness: 4
Accuracy: 5
Tone: 4
Final Agent Quality Score: 4.33



6. Files Used 
File Name-------	Purpose
metrics.py------	Defines quality metrics
judge_prompts.py---	Evaluation questions
scoring.py------	Computes final score
run_quality_eval.py-Executes Milestone 2


7. How to Execute 
python run_quality_eval.py

---------------------------------------------------------------------------------------------

**Milestone 3**

1. Task Description

The task of Milestone 3 is to modify the agent’s workflow to include a Human-in-the-Loop (HITL) checkpoint.
The agent must be able to pause execution, save its current state, and resume later without losing context.

This milestone focuses on implementing the “Saving the Game” concept in an ambient agent.



2. Implementation

A LangGraph-based agent graph was created.

A checkpoint node was added before the action execution step.

The graph execution is interrupted using:

interrupt_before = ["action_node"]


The agent’s state (memory) is saved to persistent storage using a file-based database.

On restart, the agent loads the saved state and resumes execution from the same point.




3. Execution Process

The agent starts with an initial email state.

The triage node processes the email and produces a decision.

Before taking any action, the HITL checkpoint is triggered.

The agent’s current state is saved to persistent storage.

The agent pauses execution and waits for human intervention.

On re-execution, the agent resumes from the saved state.




4. Purpose / Usage

This milestone is used to:

Allow human review and approval before critical actions

Prevent loss of agent context during pauses

Enable safe, long-running agent workflows

Support real-world scenarios where decisions require confirmation




5. Output Explanation

The output shows that:

The agent has successfully paused

The triage decision is preserved

The agent state is stored for later use

Sample Output
Agent execution paused.
Current state:
{
  "email": {
    "subject": "Urgent approval needed",
    "body": "Please approve the budget by EOD"
  },
  "triage_decision": "needs_human_review",
  "paused": true
}


This confirms that the HITL checkpoint and state persistence are working correctly.




6. Files Used:
File Name	Purpose
memory.py	-------  Saves and loads agent state
nodes.py---------	Defines agent workflow nodes
graph.py--------	Builds LangGraph with HITL
run_hitl_agent.py----	Executes the HITL agent



7. How to Execute

Run the following command from the project root:

python run_hitl_agent.py




8. Conclusion 

Milestone 3 successfully implements a Human-in-the-Loop checkpoint using LangGraph.
The agent can pause execution, persist its state, and resume later without losing information, fulfilling the “Saving the Game” requirement.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Milestone 4 – Unsafe Tool Interruption (Human-in-the-Loop)**


1. Task Description

The objective of Milestone 4 is to ensure that unsafe or sensitive tools used by the agent are not executed automatically.
Before performing such actions, the agent must pause execution and wait for human approval.

This milestone focuses on enforcing safety and control in the agent workflow.




2. Implementation

A sensitive tool (send_email) was identified and treated as unsafe.

The agent’s LangGraph workflow was modified to interrupt execution before tool execution.

The graph compilation uses:

interrupt_before = ["tools"]


A clear alert message is printed to notify the user when execution is paused.

The agent halts execution and waits for human input before proceeding.




3. Execution Process

The agent receives an email as input.

The triage node determines that a response is required.

The agent plans to use a sensitive tool (send_email).

LangGraph interrupts execution before the tools node.

The user is notified that approval is required.

The agent pauses execution and waits for human input.




4. Purpose / Usage

This milestone is used to:

Prevent unsafe automatic actions

Ensure human oversight for sensitive operations

Improve reliability and safety of the agent

Support real-world use cases involving external side-effects




5. Output Explanation

The output confirms that:

A sensitive tool was detected

Execution was paused before tool usage

The agent is awaiting human approval

Sample Output
⚠️ HUMAN APPROVAL REQUIRED ⚠️
Sensitive tool detected: send_email
Agent execution paused before tool execution.

Agent paused.
Current state:
{
  "email": {
    "subject": "Send project update",
    "body": "Please send the latest update to the client"
  },
  "triage_decision": "respond"
}




6. Files Used 
File Name	Purpose
nodes.py	Defines triage and unsafe tool logic
graph.py	Configures LangGraph interruption
run_hitl_tools_agent.py	Executes the unsafe-tool HITL workflow



7. How to Execute 

Run the following command from the project root directory:

python run_hitl_tools_agent.py




8. Workflow Summary

The agent analyzes the email.

A sensitive action is identified.

Execution is interrupted before tool usage.

The user is notified.

The agent pauses until approval is provided.




9. Conclusion 

Milestone 4 successfully ensures that unsafe tools are never executed without human approval.
By interrupting execution before tool usage, the agent enforces safety and human oversight, making it suitable for real-world applications.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------
