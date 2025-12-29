
# ReAct (Reason–Act) Loop – Code Explanation

## 1. Purpose of the ReAct Loop

The ReAct loop is responsible for **deciding what action to take and executing it** after an email has passed triage.

This loop is triggered **only when triage output allows reasoning** (`reason_act`).  
It follows a controlled **Reason → Act** workflow to avoid unnecessary actions and LLM calls.

---

## 2. Components Involved

The ReAct loop is implemented using two main components:

1. **ReasonNode** – Uses an LLM to decide the next action  
2. **ToolExecutorNode** – Executes the selected action/tool

---

## 3. Reason Node

### Class: `ReasonNode`

### Responsibility

- Analyze the email content
- Decide what action should be taken
- Return the decision in structured JSON format

---

### Model Setup

- Model: `gpt-4o-mini`
- Temperature: `0.2`
- API key loaded from environment variables

---

### Reasoning Prompt

The LLM is instructed to:

- Act as an email assistant
- Choose **one action only**
- Return **JSON and nothing else**

Expected output format:

```json
{
  "thought": "Explanation of decision",
  "action": "read_calendar | lookup_contact | reply",
  "action_input": {}
}
````

---

### Reason Node Execution Flow

### 1. Check triage result

The node first checks whether reasoning is allowed:

```python
triage_label = state.get("triage", {}).get("label")
```

If the label is not `reason_act`, reasoning is skipped.

---

#### 2. Block reasoning when not allowed

When triage blocks reasoning, the node returns a controlled output:

```json
{
  "thought": "Triage blocked reasoning",
  "action": null,
  "action_input": null
}
```

This prevents unnecessary LLM calls.

---

#### 3. Extract email content

The subject and body are extracted from the state:

```python
subject = email.get("subject", "")
body = email.get("body", "")
```

Only relevant fields are passed to the LLM.

---

#### 4. Invoke the LLM

The prompt and model are chained together, and the email content is passed as input.

---

#### 5. Parse LLM response

- The response is parsed as JSON
- If parsing fails, a fallback response is used

Fallback behavior ensures system stability:

```json
{
  "thought": "Fallback reasoning",
  "action": "reply",
  "action_input": {
    "message": "Thanks for your email!"
  }
}
```

---

#### 6. Store reasoning output

The reasoning decision is stored in the state as a list:

```json
"reasoning": [ ... ]
```

This structure allows extension to multi-step reasoning in the future.

---

## 4. Tool Executor Node

## Class: `ToolExecutorNode`

Responsibility

- Execute the action selected by the ReasonNode
- Does not perform any reasoning
- Does not use an LLM

---

### Supported Actions

| Action Name      | Behavior                     |
| ---------------- | ---------------------------- |
| `read_calendar`  | Reads calendar data          |
| `lookup_contact` | Searches contact information |
| `reply`          | Returns a direct reply       |

---

### Tool Executor Execution Flow

#### 1. Read reasoning output

The node reads the reasoning decision from the state:

```python
decision = state.get("reasoning_output", {})
```

---

#### 2. Extract action and input

```python
action = decision.get("action")
action_input = decision.get("action_input")
```

---

#### 3. Handle no-action scenario

If no action is provided, the node safely exits without executing any tool.

---

### Tool Execution Paths

#### Read Calendar

Used when meeting or scheduling information is required.

The calendar tool is invoked with a date hint (if provided).

---

#### Lookup Contact

Used to retrieve contact details based on a query string.

---

#### Reply (No Tool)

If the action is `reply`, no external tool is called.
The reply content is returned directly as output.

---

### Output Handling

The result of tool execution is stored in:

```json
"tool_result"
```

This keeps tool execution separate from reasoning logic.

---

## 5. End-to-End ReAct Flow

```text
Email
  ↓
TriageNode
  ↓
(reason_act)
  ↓
ReasonNode (LLM decides action)
  ↓
ToolExecutorNode (executes action)
  ↓
Final Agent State
```

---
