## Email Triage Module – Milestone 1  
   Project: LangGraph Email Assistant

# 1. Overview
This module implements the *triage logic* for an email assistant.
The goal is to automatically classify incoming emails into meaningful categories
so that later workflow steps can act on them.

This work corresponds to *Milestone 1* and focuses on:
- Rule-based classification
- Dataset creation
- Evaluation and accuracy reporting

No frontend or live LLM API is used in this milestone.


# 2. Triage Categories
Each email is classified into one of the following labels:

- *spam*  
  Fraud, scams, prize messages, urgent account warnings

- *promotion*  
  Discounts, offers, sales, marketing emails

- *normal*  
  Informational or conversational emails

- *action_intent*  
  Emails that require an action  
  (meetings, approvals, invoices, requests, scheduling)


# 3. Rule-Based Triage Logic
The triage logic is implemented using keyword-based rules:

# Promotion Detection
Keywords like:
discount, offer, sale, deal, free, %

# Spam Detection
Keywords like:

win, prize, reward, urgent, claim, blocked, compromised

# Action Intent Detection
Keywords like:

schedule, meeting, approve, invoice, send, book, confirm

# Normal Emails
If none of the above rules match, the email is marked as *normal*.

This approach ensures:
- No dependency on paid APIs
- Fast and deterministic classification
- Easy debugging and evaluation

# 4. Dataset (Golden Emails)
A golden dataset was created in JSON format.

Each record contains:
  json
{
  "email": "email text",
  "label": "expected category"
}

The dataset includes 30 labeled emails, covering all categories:

-Spam
-Promotion
-Normal
-Action Intent

This dataset is used only for evaluation.


5. Evaluation Logic

An evaluation script compares:

-Predicted label

-Actual (gold) label

The script outputs:

Count of each predicted class

Final accuracy score 

## Milestone 2: Test Dataset & Agent Quality Evaluation

# 1. High-Quality Test Dataset Creation
For Milestone 2, the dataset was expanded to **100+ high-quality email examples**.

The dataset includes diverse and realistic scenarios such as:
- Meeting requests
- Urgent action emails
- Promotional campaigns
- Spam and phishing attempts
- Informational and conversational messages

Each record includes:
- Email content
- Ground-truth label
- Ideal or perfect expected outcome


# 2. Data Formatting
The dataset is formatted in **JSON / CSV** to support automated testing
and integration with the evaluation framework.


# 3. Agent Quality Metrics
To evaluate the agent beyond accuracy, an **Agent Quality Score** was defined.

Key metrics include:
- **Accuracy** – Correctness of classification
- **Helpfulness** – Whether the output is useful for downstream actions
- **Tone** – Appropriate and professional handling of emails


# 4. Judge LLM Evaluation Design
A Judge LLM is conceptually defined with:
- Specific evaluation questions
- A clear scoring rubric

Scoring approaches include:
- Binary **Pass / Fail**
- Scaled **1–5 rating**

This allows structured and repeatable quality evaluation.

## Milestone 3 – Human-in-the-Loop (HITL) Safety

Project Title

Email Triage Agent with Human-in-the-Loop Safety


Objective

The goal of Milestone 3 is to introduce safety and control mechanisms into the email triage agent by identifying dangerous actions, pausing execution before such actions occur, and resuming safely after human approval. This ensures the agent does not change real-world state without explicit consent.


Understanding the Problem (Undo Test)

   Any action that changes reality and cannot be easily undone is considered dangerous.

# Dangerous Actions

-Sending emails

-Creating calendar invites

-Spending money

-Deleting files


# Safe Actions

-Reading emails

-Classifying text

-Checking or analyzing data

   This rule is known as the Undo Test.


# Dangerous Tool Identification

In this milestone, actions such as sending emails or scheduling meetings are treated as dangerous tools. These actions are explicitly tagged so the agent knows when to stop and wait for human input.


# Tagging Dangerous Actions

Each triaged email is classified with:

-A category label (spam, promotion, action_intent, etc.)

-A dangerous: true/

### Milestone 4

## Task Description
The goal of this task is to design and configure an Email Assistant that can handle conversation memory, manage multiple threads, and safely execute sensitive actions using controlled interruptions.

## Implementation Details

### 1. MemorySaver Implementation
MemorySaver is implemented to store and retrieve conversation data during the session.  
This ensures that the assistant remembers previous messages and maintains continuity.


### 2. Thread ID Management
Each conversation is assigned a unique Thread ID.  
This helps in tracking individual user conversations and prevents overlapping of messages between different sessions.


### 3. Graph Compilation Using Memory Checkpoint
The workflow graph is compiled using `checkpointer=memory`.  
This allows the system to save the current state and restore it whenever required during execution.


### 4. Session History Maintenance
Conversation history is preserved throughout the session.  
This enables the assistant to refer to earlier messages and generate accurate responses based on past context.


### 5. Unsafe Tool Identification
Sensitive tools such as email sending actions are identified as unsafe.  
These tools require explicit approval before execution to avoid unintended operations.

Examples of unsafe actions:
- Sending emails
- Performing irreversible actions


### 6. Interrupt Configuration
Interrupts are configured using the following setting:
interrupt_before = ["tools"]

This pauses the execution before any tool is called, allowing verification before continuing.


## Output
- Email Assistant maintains memory within the session  
- Conversations are handled safely using Thread IDs  
- Sensitive actions are executed only after approval  


## Conclusion
This task successfully implements a secure and memory-aware Email Assistant with controlled execution and session management.
