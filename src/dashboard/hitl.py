import streamlit as st
import json
import random
from datetime import datetime

st.set_page_config(page_title="HITL Review", layout="centered")


# ----------------------------
# LOAD EMAIL FROM YOUR JSON DATASET
# ----------------------------
def load_pending_email(path="src/data/emails.json"):
    with open(path, "r") as f:
        dataset = json.load(f)

    # pick a random email from your dataset
    item = random.choice(dataset)

    subject = item.get("subject", "No Subject")
    body = item.get("body", "")
    sender = item.get("sender", "unknown@dataset.com")
    label = item.get("human_label", "general")

    # Convert email → HITL structure
    return {
        "email": {
            "subject": subject,
            "body": body,
            "sender": sender
        },
        "triage": {
            "label": label,
            "confidence": round(random.uniform(0.75, 0.98), 2),  # fake confidence
            "source": "dataset"
        },
        "react_trace": [
            {"step": 1, "thought": f"Email classified as '{label}'."},
            {"step": 2, "action": "none"},
            {"step": 3, "observation": "Simple dataset-based classification."}
        ]
    }


# ----------------------------
# Save decision
# ----------------------------
def save_decision(decision, data):
    filename = "decision.json"
    with open(filename, "a") as f:
        f.write(json.dumps({
            "timestamp": str(datetime.now()),
            "decision": decision,
            "data": data
        }) + "\n")


# ----------------------------
# SIMPLE HITL VIEW
# ----------------------------
data = load_pending_email()

st.title("HITL Review")

# ==========================
# EMAIL
# ==========================
st.header("Email")
st.write(f"**Subject:** {data['email']['subject']}")
st.write(f"**From:** {data['email']['sender']}")
st.write("**Body:**")
st.write(data['email']['body'])

st.divider()

# ==========================
# TRIAGE
# ==========================
st.header("Triage Result")
st.json(data["triage"])

st.divider()

# ==========================
# REACT REASONING
# ==========================
st.header("Agent ReAct Output")
st.json(data["react_trace"])

st.divider()

# ==========================
# ACTION BUTTONS
# ==========================
col1, col2 = st.columns(2)

with col1:
    if st.button("Approve"):
        save_decision("approved", data)
        st.success("Approved.")

with col2:
    if st.button("Escalate"):
        save_decision("escalated", data)
        st.warning("Escalated.")
