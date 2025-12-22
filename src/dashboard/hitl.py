import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="HITL Review", layout="wide")


def load_pending_email():
    # Normally you will pass email data from triage or agent
    return {
        "email": {
            "subject": "Team meeting request",
            "body": "Can we meet tomorrow for the project update?",
            "sender": "manager@company.com"
        },
        "triage": {
            "label": "meeting_request",
            "confidence": 0.91,
            "source": "rules"
        },
        "react_trace": [
            {"step": 1, "thought": "User wants to schedule a meeting."},
            {"step": 2, "action": "read_calendar"},
            {"step": 3, "observation": "Available tomorrow at 10am, 11am"},
        ],
        "final_action": "Ask user for preferred time"
    }


# HITL UI Section

data = load_pending_email()

st.title("Human-in-the-Loop Review")
st.write("Review the agent’s reasoning and approve or escalate.")

# Show original email
st.header("Original Email")
st.json(data["email"])

# Triage decision
st.header("Triage Classification")
st.json(data["triage"])

# ReAct reasoning
st.header("ReAct Reasoning Trace")
st.json(data["react_trace"])

# Final agent action
st.header("Proposed Action")
st.success(data["final_action"])

st.divider()

# Approve / Escalate Buttons
st.subheader("Decision")

col1, col2 = st.columns(2)


def append_json_record(file_path: str, record: dict):
    try:
        # If file doesn't exist or is empty, create a new array with the record
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([record], f, ensure_ascii=False, indent=2)
                f.write("\n")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            raw = f.read().strip()

        parsed = None
        try:
            parsed = json.loads(raw) if raw else []
            if isinstance(parsed, list):
                parsed.append(record)
            else:
                # Single object -> convert to array
                parsed = [parsed, record]
        except json.JSONDecodeError:
            lines = [line for line in raw.splitlines() if line.strip()]
            objs = []
            for line in lines:
                objs.append(json.loads(line))
            parsed = objs + [record]

        # Write back as a proper JSON array (pretty-printed)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
            f.write("\n")
    except Exception as e:
        st.error(f"Failed to write JSON report: {e}")

with col1:
    if st.button("✅ Approve Action"):
        st.success("Action Approved!")
        append_json_record(
            "src/reports/approved_actions.json",
            {
                "timestamp": str(datetime.now()),
                "decision": "approved",
                "data": data,
            },
        )

with col2:
    if st.button("⚠️ Escalate to Human"):
        st.warning("Escalated for human review.")
        append_json_record(
            "src/reports/escalated_actions.json",
            {
                "timestamp": str(datetime.now()),
                "decision": "escalated",
                "data": data,
            },
        )
