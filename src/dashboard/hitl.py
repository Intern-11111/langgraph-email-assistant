import streamlit as st
import json
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

with col1:
    if st.button("✅ Approve Action"):
        st.success("Action Approved!")
        with open("approved_actions.json", "a") as f:
            f.write(json.dumps({
                "timestamp": str(datetime.now()),
                "decision": "approved",
                "data": data
            }) + "\n")

with col2:
    if st.button("⚠️ Escalate to Human"):
        st.warning("Escalated for human review.")
        with open("escalated_actions.json", "a") as f:
            f.write(json.dumps({
                "timestamp": str(datetime.now()),
                "decision": "escalated",
                "data": data
            }) + "\n")
