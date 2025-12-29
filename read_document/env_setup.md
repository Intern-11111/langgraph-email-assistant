
# ReAct (Reason–Act) Loop – Code Explanation

This document explains how to set up the development environment for the Ambient Email Agent project.

## 1. Create a Virtual Environment

Creating a virtual environment helps keep project dependencies isolated.

## On Windows

```bash
python -m venv venv
venv\Scripts\activate
````

Once activated, all Python packages will be installed inside this virtual environment.

## 2. Install Required Dependencies

Create a file named `requirements.txt` in the project root directory with the following content:

```text
langgraph
langchain
langchain-openai
python-dotenv
openai
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

## 3. Environment Variables Setup (`.env` File)

Create a `.env` file in the project root directory to store sensitive configuration values.

## Example `.env` File

```text
OPENAI_API_KEY=your_api_key_here```

```

The project uses the `python-dotenv` library to securely load environment variables at runtime.

## 4. Verify Environment Setup

To verify that the environment is correctly configured:

1. Activate the virtual environment
2. Run any Python file from the project, for example:

```bash
python main.py
```

If the script runs without errors, the environment setup is successful.

---

## 5. Project Directory Structure

A typical project directory structure for this application is shown below:

```text
project_root/
│
├── src/
│   ├── agent/
│   │   ├── react_node.py
│   │   └── tool_call.py
│   │
│   ├── triage/
│   │   ├── triage_node.py
│   │   ├── triage_rules.py
│   │   └── triage_llm.py
│   │
│   ├── data/
│   │   └── emails.json
│   │
│   ├── tools/
│   │   ├── calendar.py
│   │   └── contact.py
│   │
│   ├── dashboard/
│   │   └── hitl.py
│   │
│   └── main.py
│
├── .env
├── requirements.txt
└── README.md
```

---
