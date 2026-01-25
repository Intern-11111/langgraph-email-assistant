# Ambient Email Agent

This project is an **email assistant** built with **LangGraph + LLMs (Gemini / Hugging Face)**.

Right now it can:

- Classify an email as:
  - `ignore`
  - `notify-human`
  - `respond-act`
- If it is `respond-act`, it runs a small **ReAct loop**:
  - The LLM decides whether to **call safe mock tools** (like `read_calendar`)
  - Then drafts a reply using the tool results

This is the base for an ambient email agent that will later get HITL, memory, and real Gmail/Calendar integration.

---

## 1. Project Structure

<img width="497" height="876" alt="image" src="https://github.com/user-attachments/assets/b76efffb-e0d8-4253-8f23-201d0b09b748" />

---

## 2. LLM Config (`config.py`)

We configure chat models:

- `gemini_ai_model()` → Google Gemini chat model.  
- `hugging_face_model()` → Hugging Face chat model (optional).

API keys are loaded from `.env` using `python-dotenv`.  
Nodes call these functions to get an LLM instance.

---

## 3. State Definition (`state.py`)

Shared state that flows through the graph:


class AgentState(TypedDict):
messages: list[BaseMessage] # conversation history
mail: dict # {"subject": str, "body": str}
triage_category: Literal["ignore", "notify-human", "respond-act"]
tool_name: str | None # name of tool to call (inside ReAct)
tool_args: dict | None # arguments for that tool
final_reply: str | None # drafted reply for respond-act emails

- `messages` – chat history used by the ReAct loop.  
- `mail` – the email being processed.  
- `triage_category` – result from the triage node.  
- `tool_name` / `tool_args` – used only when the LLM wants to call a tool.  
- `final_reply` – final drafted email text for `respond-act` emails.

---

## 4. Triage Node (`node.py` – `triage_node`)

The **triage node**:

- Reads `state["mail"]["subject"]` and `state["mail"]["body"]`.  
- Calls the LLM with a prompt that explains 3 categories:

  - `ignore`: newsletters, promotions, auto-notifications  
  - `notify-human`: urgent or important, user should see it  
  - `respond-act`: needs a reply or action

- Parses the model output into a `Category` object.  
- Returns `{"triage_category": "ignore" | "notify-human" | "respond-act"}`.

`check_route` then looks at `triage_category` and routes:

- `ignore` → `ignore` node → END.  
- `notify-human` → `notify_human` node → END.  
- `respond-act` → into the ReAct loop starting at `react_model`.

---

## 5. ReAct Loop Nodes

### 5.1 ReAct model node (`react_model_node`)

This is the **"brain"** of the ReAct loop:

1. Reads `mail` and `messages` from state.  
2. Builds a `HumanMessage` with:
   - Instructions about tools (`read_calendar`, `get_user_prefs`).  
   - The email subject and body.  
3. Sends all messages to the LLM and gets back `text`.  
4. If `text` looks like JSON with `"tool"`:
   - Parse `tool_name` and `tool_args`.  
   - Set them in the state so the graph calls `react_tools`.  
5. Otherwise:
   - Treat `text` as the final reply.  
   - Set `final_reply = text` and clear `tool_name` / `tool_args`.

In simple terms:

> `react_model_node` decides: "Do we need a tool next, or can I answer now?"

### 5.2 ReAct tools node (`react_tools_node`)

This node runs **safe mock tools**:

- Checks `state["tool_name"]`.  
- If `"read_calendar"`, calls `read_calendar()` (returns fixed free slots).  
- If `"get_user_prefs"`, calls `get_user_prefs()` (returns fixed greeting/closing).  
- Appends a message like `[TOOL_RESULT] read_calendar: {...}` to `messages`.  
- Clears `tool_name` / `tool_args`.  
- Sends state back to `react_model_node`.

This creates the loop:

react_model_node → react_tools_node → react_model_node → ... → final_reply


---

## 6. Graph Flow (`graph.py`)

The LangGraph wiring:

<img width="480" height="446" alt="image" src="https://github.com/user-attachments/assets/59d217a9-0999-414c-ba71-34faf1e5e2b6" />

- `triage_node` sets `triage_category`.  
- `check_route` chooses the correct branch.  
- `respond-act` emails go into the ReAct subgraph:  
  - `react_model` ↔ `react_tools` until `final_reply` is set.

---

## 7. Notebooks

### 7.1 `01_triage_test.ipynb`

- Loads `data/test_emails.csv`.  
- Runs each email through the graph.  
- Compares `triage_category` vs the `label` in the CSV.  
- Prints accuracy and confusion matrix (Milestone 1 triage testing).

### 7.2 `02_react_agent.ipynb`

- Creates a small list/DataFrame of **respond-act style** emails.  
- For each email:
  - Calls `graph_create()` to get the workflow.  
  - Invokes the graph with an initial state.  
  - Prints:
    - The input email.  
    - The `triage_category`.  
    - The `final_reply` from the ReAct loop.

This notebook is used to **see the ReAct loop in action** and to demo the behavior to your mentor.

### 7.3 `03_evaluation.ipynb` (placeholder for later)

- Will be used in Milestone 2 to:
  - Connect to LangSmith,  
  - Upload a 100+ email dataset,  
  - Run automated evals (LLM-as-judge) on triage and replies.

---

## 8. How to Run

### 8.1 Install and set up

pip install -r requirements.txt

Create `.env` with your keys:

GOOGLE_API_KEY=your_gemini_key
HUGGINGFACEHUB_API_TOKEN=your_hf_token # optional

### 8.2 Run from terminal


You should see:

- The triage result.  
- For `respond-act`, logs from the ReAct loop and the final drafted reply.

### 8.3 Run notebooks

jupyter lab notebooks/

- Open `01_triage_test.ipynb` to test triage accuracy.  
- Open `02_react_agent.ipynb` to inspect and demo the ReAct behavior.

---

## 9. Backend API (FastAPI)

The backend is a **FastAPI** application (`backend/src/main.py`) that exposes RESTful endpoints for email processing and user authentication.

### 9.1 Key Endpoints

#### **Authentication**
- `GET /auth/login` – Initiates Google OAuth2 flow
- `GET /auth/callback` – OAuth2 callback handler, stores user tokens in PostgreSQL

#### **Email Processing**
- `POST /v1/scan-and-draft` – Scans inbox, triages emails, and generates draft replies
  - Request: `{"userid": "user@example.com"}`
  - Response: Returns email category, draft reply (if `respond-act`), and thread ID

#### **HITL Actions**
- `POST /v1/approve-action` – Approve/Edit/Deny AI-generated drafts
  - Request: `{"thread_id": "...", "action": "approve|edit|deny", "user_id": "...", "edited_text": "..."}`
  - Response: Sends email via Gmail API or marks as read

### 9.2 Run Backend Server

cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

Backend will be available at `http://localhost:8000`.

---

## 10. Frontend (Streamlit UI)

The frontend is a **Streamlit** web application (`frontend/app.py`) that provides a user-friendly interface for email management.

### 10.1 Features

- **Google OAuth Login** – Secure authentication via OAuth2
- **Email Scanning** – One-click inbox scanning
- **Draft Review** – View AI-generated replies
- **HITL Controls** – Approve, edit, or deny drafts
- **Real-time Feedback** – Category-based UI notifications

### 10.2 Run Frontend Server

streamlit run frontend/app.py --server.port 8501

Frontend will be available at `http://localhost:8501`.

---

## 11. Gmail & Calendar Integration

### 11.1 Gmail Tools (`backend/src/tools/google_gmail.py`)

- `fetch_emails()` – Fetches unread emails from user's inbox
- `send_reply()` – Sends email replies via Gmail API
- `mark_as_processed()` – Marks emails as read
- `apply_gmail_label()` – Applies custom labels (e.g., "AI-Notify")

### 11.2 Calendar Tools (`backend/src/tools/google_calendar.py`)

- `extract_event_details_llm()` – Uses LLM to detect meeting requests
- `generate_reply_llm()` – Generates replies with calendar availability

**Smart Meeting Detection:**
- If email contains meeting request → Generates reply with calendar slots
- If simple informational email → Generates brief acknowledgment (no calendar mention)

---

## 12. Database Setup (PostgreSQL)

The agent uses **PostgreSQL** for:
- **User token storage** (OAuth credentials)
- **LangGraph checkpointing** (conversation state persistence)

### 12.1 Database Schema

**1. User Tokens Table:**

```sql
CREATE TABLE user_tokens (
    user_id VARCHAR PRIMARY KEY,
    access_token VARCHAR,
    refresh_token VARCHAR,
    token_uri VARCHAR,
    client_id VARCHAR,
    client_secret VARCHAR,
    scopes VARCHAR,
    expiry TIMESTAMP
);
```

**2. LangGraph Checkpoint Tables:**

These are automatically created by `AsyncPostgresSaver.setup()` during app startup.


### 12.2 Configure Database

1. Install PostgreSQL
2. Create a database:

```bash
createdb email_assistance_db
```

3. Update `.env`:

```
DATABASE_URL=postgresql://username:password@localhost:5432/email_assistance_db
```
### 12.3 Database MetaData

<img width="746" height="748" alt="image" src="https://github.com/user-attachments/assets/9d85b804-0200-4b9d-9922-ef106e753321" />

---

## 13. Human-in-the-Loop (HITL) Workflow

The agent implements a **multi-stage HITL workflow** for user control:

### 13.1 Workflow Stages

```mermaid
graph TD
    A[Email Received] --> B[Triage Classification]
    B --> C{Category?}
    C -->|ignore| D[Mark as Read]
    C -->|notify-human| E[Label as AI-Notify]
    C -->|respond-act| F[Generate Draft Reply]
    F --> G[Pause for Human Review]
    G --> H{User Decision}
    H -->|Approve| I[Send Original Draft]
    H -->|Edit| J[Send Edited Version]
    H -->|Deny| K[Mark as Read Only]
```

### 13.2 HITL Decision Points

- **Triage Stage** – Automated (LLM classifies)
- **Draft Review Stage** – **Human approval required** (via Streamlit UI)
- **Final Action** – Human confirms send/edit/deny

This ensures the agent **never sends emails without explicit user approval**.

---

## 14. Authentication Flow

### 14.1 OAuth2 Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable APIs:
   - Gmail API
   - Google Calendar API
   - Google People API
4. Create OAuth 2.0 credentials:
   - Application type: **Web application**
   - Authorized redirect URIs: `http://localhost:8000/auth/callback`
5. Download credentials as `credentials.json`
6. Place in `credentials/credentials.json`

### 14.2 User Login Flow

1. User clicks **"Login with Google"** in Streamlit UI
2. Redirected to Google OAuth consent screen
3. After approval, redirected to `/auth/callback`
4. Backend stores tokens in PostgreSQL
5. User redirected back to Streamlit with `user_id` parameter

---

## 15. Environment Variables

Create `.env` file from `.env.example`:


Required variables:

```env
# LLM API Keys
GOOGLE_API_KEY=your_gemini_api_key_here
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here  # optional

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/email_assistance_db

# LangSmith (Optional - for monitoring)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=ambient-email-agent
```

---

## 16 Technology Stack

| Component | Technology |
|-----------|-----------|
| **LLM Framework** | LangChain + LangGraph |
| **AI Models** | Google Gemini 2.5 Flash |
| **Backend API** | FastAPI |
| **Frontend UI** | Streamlit |
| **Database** | PostgreSQL + AsyncPostgresSaver |
| **Email/Calendar** | Gmail API, Google Calendar API |
| **Authentication** | OAuth2 (Google) |
| **Monitoring** | LangSmith (optional) |

---

## 17. Testing

### 17.1 Run Unit Tests

```bash
pytest test/ -v
```

### 17.2 Available Tests

- `test_triage.py` – Triage accuracy evaluation
- `test_calendar.py` – Calendar integration tests
- `test_gmail.py` – Gmail API tests
- `test_hitl.py` – HITL workflow tests
- `test_real_api.py` – End-to-end API tests

---

## 18. Acknowledgments

- **LangChain & LangGraph** – For the agent framework
- **Google Gemini** – For LLM capabilities
- **FastAPI & Streamlit** – For web framework
- **Gmail & Calendar APIs** – For email/calendar integration

---

