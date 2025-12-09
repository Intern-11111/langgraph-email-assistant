# 🎯 What Are You Building?

You are building an Email Assistant Agent.

This AI will read emails and decide:

| Email Type    | Meaning                                                              |
| ------------- | -------------------------------------------------------------------- |
| Spam          | Fake / bad email                                                     |
| Promotion     | Offers, sale, discount                                               |
| Action Intent | Someone asking you to do something (schedule meeting, reply, follow-up) |
| Normal        | Simple message                                                       |

Later, the AI will also:

- Reason (think step-by-step)
- Take actions (like reading calendars)
- Show results in UI

But that comes later.

Right now you are building Triage = classify the email.

## 🎁 Imagine the agent is a small kid reading emails

First, the kid checks simple rules → “Does this email look like spam?”

If the kid is confused → asks a smarter adult (LLM model).

Both results are recorded.

You test how smart the agent is using a dataset.

That's the whole story ❤️

## 🏗️ Why do we create project structure?

Because your project will grow bigger and bigger.

If everything is dumped into one file → it becomes a mess.

So we organize into folders.

```
ambient-email-agent/        ← Main project folder
│── src/                    ← All source code
│    ├── agents/            ← Future agents (e.g., hello_agent)
│    ├── workflows/         ← Agent flows (ReAct later)
│    ├── triage/            ← Email classifier (you are working here)
│    ├── utils/             ← Helper files (like config)
│    └── main.py            ← Main entry of the whole app
│── data/                   ← Datasets such as golden emails
│── tests/                  ← Unit tests (later)
│── .env.sample             ← API key template
│── .gitignore              ← Files to ignore in Git
│── requirements.txt        ← Python libraries needed
│── README.md               ← Documentation for teammates
```

### 📁 src/

This is like your school bag.
Every important thing goes here.

### 📁 src/agents/

This is where your “thinking robots” live.

Example:

- `hello_agent.py` — robot that prints "Hello!"

Later:

- `react_agent.py` — robot that reasons & takes actions.

### 📁 src/workflows/

A workflow is the path the robot takes.

Like:

- Read email
- Classify email
- Do action

You will build this later.

### 📁 src/utils/

This folder has helpers.

Example:

- `config.py` → reads `.env` and loads your API keys.

Like a box where you keep tools.

### 📁 src/triage/ ← You are working here now

This folder has code that:

- Reads email
- Detects spam/promo/action
- Asks LLM if not sure
- Evaluates accuracy

Think of it as the email police department 🚓

Files:

| File               | Purpose               |
| ------------------ | --------------------- |
| `triage_node.py`   | The actual classifier |
| `evaluate_triage.py` | Tests your classifier |

### 📁 data/

This is your “notebook of examples”.

- Contains real example emails
- You label them manually
- Used to test your model

### 📁 tests/

This will have automated code tests.
(Not needed for beginner, comes later)

### 📝 .env.sample

Template that tells teammates:

“Put your API keys here.”

### 📝 .gitignore

Stops sensitive files from going to GitHub.

Examples:

- `.env`
- `refresh_token.json`
- compiled files

### 📝 requirements.txt

List of libraries your code needs.

Examples:

- langchain
- langgraph
- openai
- streamlit

### 📝 README.md

Human instructions.

## 🚦 Now… WHY are we building triage?

Imagine you receive 100 emails every day.

You don’t want the AI to:

- schedule a meeting for a spam email
- reply to a promotion email
- ignore an important meeting request

So first, we must classify the email correctly.

This is called Triage = sorting emails into bins.

Like sorting clothes:

- dirty clothes go to laundry
- good clothes go to cupboard
- torn clothes go to trash

Same for emails.

## 🛠️ Why TWO classifiers? (Rule-based + LLM)

Because:

### 🟦 Rule-based = Fast + Cheap + Simple

If the email says:

“Congratulations you won a lottery!”

→ 100% spam, no need to ask AI.

### 🟩 LLM fallback = Smart but costly

If the email is tricky:

“Hi, could you look into my previous message and update me?”

Rule-based won’t understand.
So we ask the big brain (LLM).

Combination gives:

- best accuracy
- lowest cost
- fastest speed

## 📚 Why create a dataset (Golden Email Set)?

Think of your dataset like:

- ✔ Practice questions
- ✔ Correct answers
- ✔ Used to measure accuracy

If your AI gets 40/50 correct → 80% accuracy.

This helps your mentor know:

- How well your classifier performs
- What needs improvement

## 📊 Why build evaluation script?

Because without evaluation:

- You don’t know if AI is good or bad
- You can’t improve it
- Mentor can't track progress

Evaluation uses:

- accuracy
- confusion matrix

Both tell how the model behaves.

## 🎉 Summary in Kid-Language

You are building:

| Part               | Simple Meaning                                  |
| ------------------ | ------------------------------------------------ |
| `triage_node.py`   | Your AI’s brain that sorts emails                |
| `golden_emails.json` | Practice question + answer sheet                |
| `evaluate_triage.py` | Teacher that marks AI's test                     |
| LLM fallback       | Smart adult who helps when stuck                 |
| Rule-based         | Simple rules for obvious cases                   |

Your project structure is like organizing a school bag:

- notebooks (`src`)
- assignments (`data`)
- secrets (`env`)
- tools (`utils`)
- robots (`agents`)
- workflows (`workflows`)