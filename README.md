Milestone 1 – Triage Node & Dataset

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

Milestone 2 – Agent Quality Score Evaluation


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

Milestone 3

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
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
