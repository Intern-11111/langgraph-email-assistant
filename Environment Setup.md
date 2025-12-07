# Environment Setup & API Configuration Guide

This document explains how to set up the development environment for the Ambient Email Agent project. It covers creating the virtual environment, installing dependencies, generating API keys, configuring the `.env` file, and running the Hello Agent demo.

---

## 1. Create Project Structure

Use the recommended structure:

```
ambient-email-agent/
│── src/
│    ├── agents/hello_agent.py
│    ├── workflows/
│    ├── utils/config.py
│    └── main.py
│── tests/
│── .env.sample
│── .gitignore
│── requirements.txt
│── README.md
```

---

## 2. Create a Virtual Environment

From the project root:

```bash
python -m venv ai
```

Activate it:

* **Windows:** `ai\Scripts\activate`
* **Mac/Linux:** `source ai/bin/activate`

Upgrade pip:

```bash
pip install --upgrade pip
```

---

## 3. Install Dependencies

Install all required libraries:

```bash
pip install -r requirements.txt
```

---

## 4. Setup `.env.sample` Template

Your `.env.sample` should contain:

```
OPENAI_API_KEY=
GOOGLE_API_KEY=

LANGSMITH_API_KEY=
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=ambient-agent

GMAIL_CLIENT_ID=
GMAIL_CLIENT_SECRET=
GMAIL_REFRESH_TOKEN=
```

Developers will copy this file:

```bash
cp .env.sample .env
```

Then fill in their values.

---

## 5. Get Each API Key

### 5.1 OpenAI API Key

1. Go to [https://platform.openai.com/](https://platform.openai.com/)
2. Navigate: **Dashboard → API Keys**
3. Click **Create new secret key**
4. Copy it into `.env`:

   ```
   OPENAI_API_KEY=sk-xxxx
   ```

### 5.2 Google Gemini API Key

1. Visit [https://aistudio.google.com/](https://aistudio.google.com/)
2. Go to **Get API Key**
3. Generate key
4. Add to `.env`:

   ```
   GOOGLE_API_KEY=AIza-xxxx
   ```

---

## 6. LangSmith API Setup

1. Go to: [https://smith.langchain.com/](https://smith.langchain.com/)
2. Create a project (recommended: `ambient-agent`)
3. Go to **Settings → API Keys**
4. Add to `.env`:

   ```
   LANGSMITH_API_KEY=ls-xxxx
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_PROJECT=ambient-agent
   ```

---

## 7. Setup Gmail OAuth (Client ID, Secret, Refresh Token)

### 7.1 Create Google Cloud Project

1. Visit [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Create new project: `ambient-email-agent`

### 7.2 Enable Gmail API

`APIs & Services → Library → Gmail API → Enable`

### 7.3 Configure OAuth Consent Screen

1. `APIs & Services → OAuth consent screen`
2. Choose **External** (Testing)
3. Add your email as **Test User**
4. Save

### 7.4 Create OAuth Client ID

1. Go to **Credentials**
2. Click **Create Credentials → OAuth client ID**
3. Choose **Desktop App**
4. Download `client_secret.json`

### 7.5 Generate GMAIL_REFRESH_TOKEN

1. Place `client_secret.json` inside `tools/`
2. Run the utility script:

   ```bash
   python tools/get_gmail_refresh_token.py
   ```
3. Browser opens → log in → allow permissions
4. Copy printed values into `.env`:

   ```
   GMAIL_CLIENT_ID=
   GMAIL_CLIENT_SECRET=
   GMAIL_REFRESH_TOKEN=
   ```

---

## 8. Config File Setup (`config.py`)

Create file:

```
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
GMAIL_REFRESH_TOKEN = os.getenv("GMAIL_REFRESH_TOKEN")
```

---

## 9. Hello Agent Script Setup

`src/agents/hello_agent.py`:

```python
from langchain_openai import ChatOpenAI
from src.utils.config import OPENAI_API_KEY

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini")

def hello_agent():
    return llm.invoke("Hello! Respond with: Hello Agent works!")
```

---

## 10. Run the Hello Agent

Example: `src/main.py`:

```python
from agents.hello_agent import hello_agent

if __name__ == "__main__":
    print(hello_agent())
```

Run it:

```bash
python src/main.py
```

If everything is correct, you should see:

```
Hello Agent works!
```

---

## 11. Final Checklist

* [ ] Virtual environment created
* [ ] Dependencies installed
* [ ] `.env` configured
* [ ] OpenAI key added
* [ ] Google API key added
* [ ] LangSmith enabled
* [ ] Gmail OAuth values generated
* [ ] Hello Agent works

---

This completes the initial setup for all teammates.
