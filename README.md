# LangGraph Email Assistant

An ambient email assistant built with LangGraph and a ReAct-style reasoning loop. It processes incoming emails, consults tools (calendar, contacts), and proposes actions. A simple Human-in-the-Loop (HITL) dashboard lets you review the agent’s reasoning and approve or escalate actions. The repo also includes evaluation assets to iterate on quality.

---

## Highlights

- ReAct-based agent (`agents/react_loop.py`) orchestrated by `src/main_ReAct.py`
- Tooling: calendar lookup and contact lookup
- Optional Excel export of agent outputs
- HITL dashboard in Streamlit for quick reviews
- Evaluation datasets and prompts for further analysis

---

## Requirements

- Python 3.11 recommended
- A virtual environment (venv)
- API keys as needed (e.g., OpenAI)

Install dependencies:

```bash
pip install -r requirements.txt
```

Note: Excel export uses `openpyxl`. If you plan to export to Excel, install it:

```bash
pip install openpyxl
```

---

## Quick Start

1) Create and activate a venv (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Set environment variables (as needed):

```powershell
$env:OPENAI_API_KEY="your_openai_key"
# Optional: $env:LANGSMITH_API_KEY="your_langsmith_key"
```

3) Run the agent:

```powershell
python src\main_ReAct.py "Meeting request" "Can we schedule for tomorrow?"
```

The script prints a structured trace of the agent’s reasoning and proposed action. It will prompt to export results to Excel if `openpyxl` is available.

---

## HITL Dashboard

Interactive review UI to approve or escalate proposed actions.

Run with Streamlit:

```powershell
streamlit run src\dashboard\hitl.py
```

Actions are recorded to JSON files for audit:

- Approved: [src/reports/approved_actions.json](src/reports/approved_actions.json)
- Escalated: [src/reports/escalated_actions.json](src/reports/escalated_actions.json)

---

## Configuration

- General config: [src/utils/config.py](src/utils/config.py)
- Data samples: [data/test_emails.csv](data/test_emails.csv), [data/golden_emails.json](data/golden_emails.json)
- Credentials: Google OAuth secrets and Gmail creds live under [tools](tools) in this repo structure. Do not commit real credentials.

Environment variables commonly used:

- `OPENAI_API_KEY`: for LLM calls
- `LANGSMITH_API_KEY` (optional): for experiment tracking
- Google API OAuth tokens (optional): if integrating Gmail/Calendar

Use a `.env` file with `python-dotenv`, or set variables in your shell.

---

## Project Structure (key files)

```
src/
  main_ReAct.py              # CLI entry for agent run
  agents/
    react_loop.py            # ReAct agent implementation
  tools/
    calendar.py              # Calendar helper
    contact.py               # Contact lookup helper
  dashboard/
    hitl.py                  # Streamlit HITL UI
  evaluation/
    eval/                    # Evaluators or scripts (iterative)
    Metrics/                 # Metric definitions or reports
    prompt/                  # Prompt assets for evaluation
reports/
  approved_actions.json      # HITL approvals
  escalated_actions.json     # HITL escalations
data/
  test_emails.csv            # Sample evaluation set
  golden_emails.json         # Ideal responses for comparison
```

Note: Some files are placeholders or examples to bootstrap workflows. Align naming as you develop.

---

## Running Tips

- From the repo root, `python src\main_ReAct.py` ensures imports resolve (`agents/...`).
- If you see import errors, run via module or adjust `PYTHONPATH`:
  - `python -m src.main_ReAct "Subject" "Body"`
- For Excel export, answer the prompt and ensure the destination directory is writable.

---

## Evaluation (optional)

The `evaluation/` folder contains datasets, metrics, and prompts to design evaluators. If you use LangSmith or other judge frameworks, wire them here and record results under `reports/`.

Suggested approach:

1. Define metrics (accuracy, helpfulness, tone)
2. Build an evaluator script under `evaluation/eval/`
3. Compare agent outputs against `golden_emails.json`
4. Track summaries under `reports/`

---

## Troubleshooting

- Missing package: run `pip install -r requirements.txt` and add extras like `openpyxl`.
- Streamlit not found: `pip install streamlit`.
- Windows execution policy blocks `Activate.ps1`: run PowerShell as admin and `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`.
- Credential errors: ensure test credentials are placeholders; never commit real secrets.

---

## Disclaimer

This repository is for educational and internship purposes. Do not use with real customer data or production credentials without appropriate reviews and security hardening.