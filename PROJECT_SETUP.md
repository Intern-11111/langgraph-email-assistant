# Project Setup Guide - Ambient Email Agent

**Complete Installation and Configuration Instructions**

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Configuration](#configuration)
- [Google Cloud Setup](#google-cloud-setup)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Development Workflow](#development-workflow)

---

## ✅ Prerequisites

### System Requirements
- **Operating System:** Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python:** 3.9 or higher
- **Memory:** Minimum 4GB RAM (8GB recommended)
- **Disk Space:** At least 2GB free space

### Required Accounts
1. **Google Cloud Account** - For Gmail/Calendar API access
2. **Google Gemini API Key** - For LLM capabilities
3. **LangSmith Account** (Optional) - For tracing and monitoring

### Check Python Version
```bash
python --version
# or
python3 --version
```

**Expected Output:** `Python 3.9.x` or higher

---

## 📥 Installation Steps

### Step 1: Clone/Download the Project

```bash
# If using git
cd "d:\Aayush\College\Interships\Infosys-Building an Ambient Agent"
cd A1-email-agent\final

# Or navigate to the project folder if already downloaded
```

---

### Step 2: Create Virtual Environment

**Why?** Isolates project dependencies from system Python packages.

#### On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**Verify Activation:**
You should see `(venv)` prefix in your terminal:
```
(venv) C:\path\to\project>
```

---

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**What gets installed:**
- LangGraph & LangChain - Agent framework
- FastAPI & Uvicorn - Backend server
- Streamlit - Frontend UI
- Transformers & PyTorch - ML models
- Google API clients - Gmail/Calendar integration
- AsyncPG - Database connector
- And more...

**Expected Time:** 2-5 minutes depending on internet speed

---

### Step 4: Verify Installation

```bash
# Check if key packages are installed
python -c "import langchain; import streamlit; import fastapi; print('✅ All core packages installed')"
```

**Expected Output:** `✅ All core packages installed`

---

## ⚙️ Configuration

### Step 1: Create Environment File

Copy the example environment file:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

---

### Step 2: Configure API Keys

Open `.env` file in a text editor and fill in your credentials:

```env
# ============================================
# LLM API Keys
# ============================================
GOOGLE_API_KEY=your_gemini_api_key_here
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here  # Optional

# ============================================
# Database Configuration
# ============================================
# For Development (SQLite - no setup needed)
DATABASE_URL=sqlite:///./email_agent.db

# For Production (PostgreSQL)
# DATABASE_URL=postgresql://username:password@localhost:5432/email_assistance_db

# ============================================
# LangSmith (Optional - for monitoring)
# ============================================
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_key_here
LANGCHAIN_PROJECT=ambient-email-agent

# ============================================
# Application Settings
# ============================================
APP_ENV=development
DEBUG=true
```

---

### Step 3: Get Google Gemini API Key

1. Visit: https://ai.google.dev/
2. Click **"Get API Key"**
3. Create a new project or select existing
4. Generate API key
5. Copy the key and paste into `.env` as `GOOGLE_API_KEY`

**Free Tier Limits:**
- 60 requests per minute
- Sufficient for development and testing

---

### Step 4: Get LangSmith API Key (Optional)

1. Visit: https://smith.langchain.com/
2. Sign up or log in
3. Go to **Settings** → **API Keys**
4. Create new API key
5. Copy and paste into `.env` as `LANGCHAIN_API_KEY`

**Benefits:**
- Full trace visibility for debugging
- Performance monitoring
- Evaluation dataset management

---

## ☁️ Google Cloud Setup

### Required for: Gmail & Calendar Integration

#### Step 1: Create Google Cloud Project

1. Go to: https://console.cloud.google.com/
2. Click **"Select a project"** → **"New Project"**
3. **Project Name:** `Email-Agent-Project` (or your choice)
4. Click **"Create"**

---

#### Step 2: Enable Required APIs

1. In Google Cloud Console, go to **"APIs & Services"** → **"Library"**
2. Search and enable the following APIs:
   - ✅ **Gmail API**
   - ✅ **Google Calendar API**
   - ✅ **Google People API** (for contacts)

**For each API:**
- Click on it → Click **"Enable"**

---

#### Step 3: Create OAuth 2.0 Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**

**If prompted to configure consent screen:**
- User Type: **External**
- App name: `Email Agent`
- User support email: Your email
- Developer contact: Your email
- Click **"Save and Continue"** through all steps

**Back to creating OAuth client:**
3. Application type: **Web application**
4. Name: `Email Agent OAuth Client`
5. **Authorized redirect URIs:**
   ```
   http://localhost:8000/auth/callback
   ```
6. Click **"Create"**

---

#### Step 4: Download Credentials

1. After creation, click **Download JSON** (download icon)
2. Rename the downloaded file to `credentials.json`
3. Place it in the project folder:
   ```
   final/
   └── credentials/
       └── credentials.json
   ```

**File Structure:**
```
final/
├── backend/
├── frontend/
├── credentials/
│   └── credentials.json  ← Place here
├── .env
└── ...
```

---

## 🗄️ Database Setup

### Option 1: SQLite (Recommended for Development)

**No setup needed!** SQLite database file will be created automatically on first run.

The database file will be created at: `./email_agent.db`

---

### Option 2: PostgreSQL (Recommended for Production)

#### Windows Installation:

1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run installer (recommended: version 14 or higher)
3. During installation:
   - Set password for `postgres` user (remember this!)
   - Port: `5432` (default)
   - Locale: Default

#### macOS Installation:

```bash
# Using Homebrew
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14
```

#### Linux (Ubuntu) Installation:

```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

---

#### Create Database

```bash
# Switch to postgres user (Linux/macOS)
sudo -u postgres psql

# On Windows, open "SQL Shell (psql)" from Start Menu
```

Then run these SQL commands:

```sql
-- Create database
CREATE DATABASE email_assistance_db;

-- Create user (optional, for security)
CREATE USER email_agent WITH PASSWORD 'your_secure_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE email_assistance_db TO email_agent;

-- Exit
\q
```

---

#### Update Environment File

Update your `.env` file with PostgreSQL connection:

```env
DATABASE_URL=postgresql://email_agent:your_secure_password@localhost:5432/email_assistance_db
```

---

#### Verify Database Connection

```bash
# Test connection
python -c "from backend.src.db import get_database_connection; print('✅ Database connected')"
```

---

## 🚀 Running the Application

### Step 1: Start the Backend Server

Open a terminal in the project directory:

```bash
# Make sure virtual environment is activated
# You should see (venv) in terminal

# Navigate to backend directory
cd backend

# Start FastAPI server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal running!** ✅

---

### Step 2: Start the Frontend Server

Open a **NEW terminal window** (keep backend running):

```bash
# Navigate to project directory
cd final

# Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Start Streamlit frontend
streamlit run frontend/app.py --server.port 8501
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**Browser should auto-open!** If not, visit: http://localhost:8501

---

### Step 3: First Login

1. In the Streamlit interface, click **"Login with Google"**
2. You'll be redirected to Google OAuth consent screen
3. **Select your Google account**
4. Review permissions:
   - ✅ Read email messages
   - ✅ Send email on your behalf
   - ✅ View and manage calendar
5. Click **"Allow"**
6. You'll be redirected back to the application

**First-time setup complete!** 🎉

---

## 🧪 Testing

### Run Unit Tests

```bash
# From project root directory
pytest test/ -v
```

**Expected Output:**
```
test/test_triage.py::test_triage_accuracy PASSED     [ 10%]
test/test_hitl.py::test_pause_mechanism PASSED       [ 20%]
test/test_calendar.py::test_calendar_tool PASSED     [ 30%]
...
======================== X passed in Y.YYs ========================
```

---

### Run Specific Test Files

```bash
# Test triage only
pytest test/test_triage.py -v

# Test HITL workflow
pytest test/test_hitl.py -v

# Test integration
pytest test/test_integration.py -v
```

---

### Test with Sample Email

Create a test file `test_email.json`:

```json
{
  "subject": "Meeting Request",
  "from": "test@example.com",
  "body": "Can we schedule a call next Tuesday at 2 PM?"
}
```

Run manual test:

```bash
python -c "
from backend.src.graph import graph_create
import json

with open('test_email.json', 'r') as f:
    email = json.load(f)

graph = graph_create()
result = graph.invoke({'mail': email})
print(result)
"
```

---

## 🔧 Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
# Ensure virtual environment is activated
# Check if packages are installed
pip list

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

---

### Issue: Backend server won't start

**Error:** `Address already in use`

**Solution:**
```bash
# Windows - Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>

# Or use a different port
uvicorn src.main:app --reload --port 8001
```

---

### Issue: Gmail API "Access Denied"

**Possible Causes:**
1. `credentials.json` not in correct location
2. Redirect URI mismatch
3. APIs not enabled in Google Cloud

**Solution:**
1. Verify `credentials.json` is in `credentials/` folder
2. Check Google Cloud Console → Credentials → Authorized redirect URIs
   - Must include: `http://localhost:8000/auth/callback`
3. Verify APIs are enabled: Gmail API, Calendar API

---

### Issue: Database connection failed

**SQLite:**
```bash
# Check if file exists and permissions
ls -la email_agent.db

# If corrupted, delete and restart
rm email_agent.db
```

**PostgreSQL:**
```bash
# Test connection manually
psql -h localhost -p 5432 -U email_agent -d email_assistance_db

# If connection refused, check if PostgreSQL is running
# Windows: Check Services
# macOS/Linux:
sudo systemctl status postgresql
```

---

### Issue: LangSmith tracing not working

**Check:**
1. `LANGCHAIN_TRACING_V2=true` in `.env`
2. `LANGCHAIN_API_KEY` is correct
3. Project name matches LangSmith dashboard

**Test connection:**
```bash
python -c "
from langsmith import Client
client = Client()
print('✅ LangSmith connected')
"
```

---

### Issue: Streamlit shows "Connection Error"

**Solutions:**
1. Check backend is running on port 8000
2. Verify `.env` file exists and is loaded
3. Check browser console for specific errors (F12)

**Test backend directly:**
```bash
curl http://localhost:8000/
# Should return: {"message": "Email Agent API"}
```

---

## 👨‍💻 Development Workflow

### Daily Startup Routine

1. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Start backend** (Terminal 1)
   ```bash
   cd backend
   uvicorn src.main:app --reload --port 8000
   ```

3. **Start frontend** (Terminal 2)
   ```bash
   streamlit run frontend/app.py --server.port 8501
   ```

4. **Check LangSmith traces** (Optional)
   - Visit: https://smith.langchain.com/
   - Select your project
   - View traces for debugging

---

### Making Changes

#### Modify Agent Logic
1. Edit files in `backend/src/`
2. Server auto-reloads (if using `--reload` flag)
3. Test changes in Streamlit UI

#### Modify UI
1. Edit `frontend/app.py`
2. Streamlit auto-reloads on save
3. Refresh browser to see changes

#### Add New Tools
1. Create tool function in `backend/src/tools/`
2. Tag as safe or dangerous
3. Add to graph's available tools
4. Update tests in `test/`

---

### Testing Your Changes

```bash
# Run full test suite
pytest test/ -v

# Run specific test
pytest test/test_your_feature.py -v

# Run with coverage report
pytest test/ --cov=backend --cov-report=html
```

---

### Debugging with LangSmith

1. Ensure tracing is enabled in `.env`
2. Run your test/operation
3. Go to LangSmith dashboard
4. Click on latest run
5. Inspect:
   - Node execution order
   - Input/output at each step
   - LLM prompts and responses
   - Tool calls and results

---

## 📁 Project Structure Overview

```
final/
├── backend/
│   └── src/
│       ├── main.py              # FastAPI app
│       ├── graph.py             # LangGraph workflow
│       ├── state.py             # State schema
│       ├── node.py              # Graph nodes
│       ├── tools/               # Tool implementations
│       └── HITL/                # HITL logic
│
├── frontend/
│   └── app.py                   # Streamlit UI
│
├── triage/
│   ├── triage_node.py           # Classification logic
│   └── triage_model/            # Trained ML model
│
├── evaluation/
│   ├── judge_evaluation.py      # LLM-as-a-judge
│   └── metrics.py               # Quality metrics
│
├── test/
│   └── test_*.py                # Test suite
│
├── data/
│   └── test_emails.csv          # Test dataset
│
├── credentials/
│   └── credentials.json         # OAuth credentials
│
├── .env                         # Environment variables
├── requirements.txt             # Dependencies
└── README.md                    # Project overview
```

---

## 🎓 Next Steps

### After Successful Setup:

1. **Explore the UI**
   - Click "Scan Inbox" to test with your emails
   - Review generated drafts
   - Test Approve/Edit/Deny controls

2. **Check LangSmith Traces**
   - View execution flow
   - Understand decision-making
   - Debug any issues

3. **Run Evaluation**
   ```bash
   python run_evaluator.py
   ```
   - Test against 100+ email dataset
   - See quality metrics
   - Identify improvement areas

4. **Read Component Documentation**
   - [README.md](README.md) - Full project overview
   - [TEAM_CONTRIBUTIONS.md](TEAM_CONTRIBUTIONS.md) - Who built what

---

## 📞 Support

### Getting Help

If you encounter issues:

1. **Check this guide** - Most common issues covered
2. **View error logs** - Check terminal output for specific errors
3. **LangSmith traces** - Debug agent behavior
4. **Test suite** - Run tests to verify components
5. **Team documentation** - Individual README files have component details

---

## ✅ Setup Checklist

Use this checklist to verify your setup:

- [ ] Python 3.9+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with API keys
- [ ] Google Cloud project created
- [ ] Gmail & Calendar APIs enabled
- [ ] OAuth credentials downloaded (`credentials.json`)
- [ ] Database configured (SQLite or PostgreSQL)
- [ ] Backend server starts successfully
- [ ] Frontend UI loads in browser
- [ ] Google OAuth login works
- [ ] Test suite passes (`pytest test/`)

---

**Setup Complete!** 🎉

You're now ready to use and develop the Ambient Email Agent. Enjoy exploring the project!

---

*For questions about specific components, refer to individual team member documentation or the main README.*
