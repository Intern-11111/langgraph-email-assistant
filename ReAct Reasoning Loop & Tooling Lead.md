# ReAct Agent Module — Design, Necessity & Implementation Guide

This document explains **why** the ReAct reasoning loop is needed, what each file does, and how the entire system works end‑to‑end inside the `ambient-email-agent` project.

It is written for beginners so you can follow the flow clearly.

---

# ⭐ Why Do We Need a ReAct Agent?

The project is an **Email Assistant**. After an email is classified by the **Triage System**, we need the system to:

* think about the email (“Reason”)
* decide what action to take (“Act”)
* call tools (calendar, contacts, etc.)
* observe results
* decide the final output

This cycle is called **ReAct** → **Reason + Act + Observe + Repeat**.

LangGraph helps orchestrate nodes, but before using it we create a **simple local ReAct agent**:

* easy to test
* safe (mock tools only)
* produces clean JSON traces
* perfect for learning how reasoning loops work

---

# 📁 Project Files Added

```
ambient-email-agent/
└── src/
    ├── agents/
    │    └── react_loop.py
    ├── tools/
    │    ├── calendar.py
    │    └── contacts.py
    └── main_react.py
```

Each file plays an important role.

---

# 🧩 File 1: tools/calendar.py — Mock Calendar Tool

### Purpose

This tool simulates a user calendar.
The agent can "read the calendar" to:

* find available meeting slots
* see existing events
* prepare smart suggestions

### Why is it mocked?

Because during development:

* We don't want to connect to Google Calendar.
* We need predictable outputs for debugging.
* It helps us understand tool‑calling before real APIs.

### What it returns

* List of available times
* A few mock events
* A helpful note if the email included a date hint

This tool represents the idea that agents "use real-world functions to act."

---

# 🧩 File 2: tools/contacts.py — Mock Contact Lookup Tool

### Purpose

Many emails involve people:

* "Who is Alice?"
* "Find Bob’s email"
* "Contact the manager"

This tool provides:

* mock contact data (name, email, phone)
* simple lookup behavior

Just like the calendar tool, it makes learning easier and safer.

---

# 🧠 File 3: agents/react_loop.py — The Agent’s Brain

This is the **core ReAct loop implementation**.

### What the agent does:

1. **Thinks** (internal reasoning string)
2. **Decides**: call tool or finish
3. **Acts**: executes a calendar or contacts tool
4. **Observes** tool result
5. Repeats until confident enough to finish

### Why it exists

A good AI assistant must:

* analyze email content
* plan actions
* use tools
* return a final action

This file simulates all of that with clean logs.

### Output

The agent produces a JSON trace containing:

* trace_id
* timestamps
* all chain-of-thought steps (safe, short version)
* actions + parameters
* tool observations
* final recommended action

This trace is later used by:

* LangSmith
* HITL UI (human approval)
* Debugging & evaluation

---

# 🖥️ File 4: main_react.py — CLI Runner

### Purpose

Allows you to test the agent locally:

```
python src/main_react.py "Subject" "Body"
```

### What it does

* Creates a `ReactAgent` instance
* Runs the agent on the given email
* Prints neatly formatted JSON output

### Why it’s needed

* You can run and debug without any UI
* Perfect for testing before integrating into LangGraph
* Everyone in the team can run the same command and reproduce your results

---

# 🔄 How All the Pieces Work Together

```
Email → ReAct Loop → Tool Calls → Observations → Final Action (JSON)
```

### Example flow

1. User sends an email: "Can we schedule a meeting tomorrow?"
2. ReAct agent detects keywords: *schedule, meeting*
3. Calls **read_calendar** to check available slots
4. Observes slots: "Tomorrow 10am, 11am, 2pm"
5. Produces final message:
   → "Suggest reply asking for preferred time"
6. Creates a **trace** for debugging and UI

This is exactly how modern AI agents behave.

---

# 📚 Why We Write ReAct Before Using LangGraph

LangGraph Workflow Later:

* Nodes: Triage → ReAct → Tools → HITL
* Edges: connecting node outputs to next node
* Event streaming

But before that, you must understand:

* How reasoning works
* How tools are called
* How output is structured

The code here gives that foundation.

---

# 🧪 Testing the Agent

From project root:

```
python src/main_react.py "Meeting request" "Can we meet this week?"
```

You will see:

* reasoning steps
* tools called
* final recommended action

This proves the agent loop is working **correctly**.

---

# ✔️ Summary

This ReAct module is critical because it:

* Represents the **brain** of the email assistant
* Demonstrates **reason + action** loops
* Teaches tool-based AI behavior
* Prepares for LangGraph integration
* Produces trace logs for debugging & UI display

Once triage + react modules are done, we will combine them, add HITL UI, and connect to LangSmith.

You now have a complete, beginner-friendly ReAct foundation usable by your whole team.
