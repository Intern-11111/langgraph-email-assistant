
# Triage System Documentation

## 1. Overview

The triage system is responsible for **classifying incoming emails** into **three action categories**:

- **ignore** – No action needed
- **notify_human** – Requires human attention
- **reason_act** – Needs automated reasoning or action

The system uses a **hybrid approach** combining **rule-based triage** and **LLM fallback** to improve accuracy and flexibility.

---

## 2. Rule-Based Triage

### Class: `RuleBasedTriage`

**Purpose:** Quickly classify emails based on keyword rules.  

**Returns:** Dictionary with keys:

```python
{
  "label": "ignore/notify_human/reason_act",
  "confidence": float
}
````

### Logic

1. **IGNORE category:**
   Detects promotional, spam, or newsletter emails using keywords:

   "unsubscribe", "spam", "lottery", "promotion", "newsletter"
   Confidence: `0.95`

2. **NOTIFY_HUMAN category:**
   Detects emails requiring human attention based on urgency or complaints:

   "urgent", "complaint", "angry", "issue", "problem", "fail", "refund"
   Confidence: `0.90`

3. **REASON/ACT category:**
   Detects actionable emails like meetings or questions:

   "meeting", "schedule", "call", "zoom", "availability", "contact", "email", "question"
   Confidence: `0.85`

4. **Fallback:**
   If none of the above matches, default to:

```python
{"label": "reason_act", "confidence": 0.60}
```

---

## 3. LLM Fallback Triage

### Class: `LLMFallbackTriage`

**Purpose:** Handles emails not confidently classified by rules using a **large language model** (LLM).

### Features

- Uses `gpt-4o-mini` via LangChain
- Returns the same three categories as rules (`ignore`, `notify_human`, `reason_act`)
- Provides a **confidence score** for each classification

### Workflow

1. Construct a prompt for the LLM with the email **subject and body**
2. Ask the LLM to classify into **one of the three categories**
3. Parse the **JSON response** from the model
4. Validate output:

   - If label is invalid → fallback to `"reason_act"`
   - Confidence is clamped between 0.0 and 1.0

**Fallback ensures:** No email goes unclassified, even if rules fail.

---

## 4. Triage Node

### Class: `TriageNode`

**Purpose:** Main node that integrates **rule-based triage** and **LLM fallback**.

### Attributes

- `threshold`: Minimum confidence for rule-based triage before calling LLM
- `rules`: Instance of `RuleBasedTriage`
- `llm`: Instance of `LLMFallbackTriage`

### Methods

1. **run(email)**

- Input: `email` dictionary with keys `subject`, `body`, `sender`
- Process:

  1. Apply rule-based triage
  2. If `confidence >= threshold` → use rule label
  3. Else → call LLM for classification
- Returns a dictionary:

```python
{
  "final_label": "<ignore|notify_human|reason_act>",
  "final_confidence": float,
  "source": "rules" | "llm"
}
```

2 **triage_node(state)**

- Input: `state` dictionary with key `"email_text"`
- Adds `"triage_result"` to state with final classification

3 ****call**(state)**

- Allows the node to be called like a function, returning updated state

---

## 5. How It Works Together

1. **Initial Processing:** Email text is sent to `TriageNode`.
2. **Rule Evaluation:** `RuleBasedTriage.classify()` checks for keyword matches.
3. **Threshold Check:**

   - If rules are confident → return label
   - Else → fallback to `LLMFallbackTriage.classify()`
4. **Output:** `TriageNode` returns structured state for the pipeline:

```json
{
  "email_text": { "subject": "...", "body": "...", "sender": "..." },
  "triage_result": { "final_label": "...", "final_confidence": 0.xx, "source": "rules|llm" }
}
```
