Email Triage Module – Milestone 1  
   Project: LangGraph Email Assistant

## 1. Overview
This module implements the *triage logic* for an email assistant.
The goal is to automatically classify incoming emails into meaningful categories
so that later workflow steps can act on them.

This work corresponds to *Milestone 1* and focuses on:
- Rule-based classification
- Dataset creation
- Evaluation and accuracy reporting

No frontend or live LLM API is used in this milestone.

---

## 2. Triage Categories
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

---

## 3. Rule-Based Triage Logic
The triage logic is implemented using keyword-based rules:

### Promotion Detection
Keywords like:
discount, offer, sale, deal, free, %

### Spam Detection
Keywords like:

win, prize, reward, urgent, claim, blocked, compromised

### Action Intent Detection
Keywords like:

schedule, meeting, approve, invoice, send, book, confirm

### Normal Emails
If none of the above rules match, the email is marked as *normal*.

This approach ensures:
- No dependency on paid APIs
- Fast and deterministic classification
- Easy debugging and evaluation

## 4. Dataset (Golden Emails)
A golden dataset was created in JSON format.

Each record contains:
  json
{
  "email": "email text",
  "label": "expected category"
}

The dataset includes 30 labeled emails, covering all categories:

Spam
Promotion
Normal
Action Intent

This dataset is used only for evaluation.


5. Evaluation Logic

An evaluation script compares:

Predicted label

Actual (gold) label

The script outputs:

Count of each predicted class

Final accuracy score 

## Milestone 2: Test Dataset & Agent Quality Evaluation

### 1. High-Quality Test Dataset Creation
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

---

### 2. Data Formatting
The dataset is formatted in **JSON / CSV** to support automated testing
and integration with the evaluation framework.

---

### 3. Agent Quality Metrics
To evaluate the agent beyond accuracy, an **Agent Quality Score** was defined.

Key metrics include:
- **Accuracy** – Correctness of classification
- **Helpfulness** – Whether the output is useful for downstream actions
- **Tone** – Appropriate and professional handling of emails

---

### 4. Judge LLM Evaluation Design
A Judge LLM is conceptually defined with:
- Specific evaluation questions
- A clear scoring rubric

Scoring approaches include:
- Binary **Pass / Fail**
- Scaled **1–5 rating**

This allows structured and repeatable quality evaluation.