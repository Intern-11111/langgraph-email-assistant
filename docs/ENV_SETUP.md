Environment Setup Guide
This document outlines the steps to set up the development environment, install dependencies, and run the project locally.

Prerequisites
Python 3.10+ (Ensure Python is added to your system PATH)

Git (For version control)

Virtual Environment (venv) (Recommended to isolate dependencies)

1. Clone the Repository

git clone <https://github.com/Intern-11111/langgraph-email-assistant.git>
cd langgraph-email-assistant
2. Environment Initialization
It is critical to run this project in an isolated virtual environment to prevent dependency conflicts.

Create the Virtual Environment

# Windows
python -m venv venv

Activate the Virtual Environment

# Windows
venv\Scripts\activate
Note: Your command prompt should now show (venv) indicating the environment is active.

3. Install Dependencies
All core libraries for the agent, server, and evaluation metrics are locked in requirements.txt.

pip install -r requirements.txt
Key Libraries Installed

LangChain / LangGraph: Agent orchestration and graph-based workflows.

4. Environment Variables
Create a .env file in the root directory to manage sensitive configuration.

touch .env
Required Variables: Currently, the basic triage uses heuristics and local models. If external LLM providers (like OpenAI or Anthropic) are integrated later, add their keys here.

Code snippet

# .env file content
# ENV=development
# Gemini_api_key=your_key_here (Future use)
Note: The .gitignore is already configured to exclude .env and venv/ from version control.

5. Running the Application
Start the FastAPI Server
The server hosts the triage agent and evaluation endpoints.

python run_server.py
Server will start at: http://127.0.0.1:8000

Interactive API Docs: http://127.0.0.1:8000/docs

Verify Installation
To confirm the system is working, navigate to the /docs endpoint in your browser and test the Health Check or Triage endpoints.

6. Project Structure Overview
Plaintext

langgraph-email-assistant
├── src/                  # Core application and agent logic
├── run_server.py         # FastAPI server entry point
├── requirements.txt      # Python dependencies
├── README.md             # Project overview
├── ENV.md                # This setup guide
└── .gitignore            # Git configuration