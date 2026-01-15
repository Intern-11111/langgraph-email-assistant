import streamlit as st
import sys
import os
import time
from datetime import datetime

# ------------------------------------------------
# Import agent logic
# ------------------------------------------------
sys.path.append(os.path.abspath("src"))
from agent import run_email_agent   # respond / ignore / notify_human

# ------------------------------------------------
# Absolute path setup for edited emails (IMPORTANT)
# ------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
EDITED_EMAIL_FILE = os.path.join(DATA_DIR, "edited_emails.log")

os.makedirs(DATA_DIR, exist_ok=True)

# ------------------------------------------------
# Helper: Context Analysis (Milestone 4)
# ------------------------------------------------
def analyze_email_context(email: str) -> str:
    email = email.lower().strip()

    if email == "":
        return "empty"

    casual_keywords = [
        "cricket", "movie", "match", "game", "play",
        "party", "hi", "hello", "hey", "bro", "lol"
    ]

    if any(word in email for word in casual_keywords):
        return "irrelevant"

    ambiguous_phrases = [
        "please do the needful",
        "please be needful",
        "as discussed",
        "kindly check",
        "let me know",
        "do the needful"
    ]

    if any(phrase in email for phrase in ambiguous_phrases):
        return "ambiguous"

    return "relevant"

# ------------------------------------------------
# Page Config
# ------------------------------------------------
st.set_page_config(page_title="LangGraph Email Assistant", layout="centered")
st.title("📧 LangGraph Email Assistant")
st.write("Human-in-the-Loop Email Triage (Milestone 3 & 4)")

# ------------------------------------------------
# Session State
# ------------------------------------------------
if "paused" not in st.session_state:
    st.session_state.paused = False

if "email_text" not in st.session_state:
    st.session_state.email_text = ""

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# ------------------------------------------------
# Email Input
# ------------------------------------------------
email_text = st.text_area(
    "✉️ Enter Email Content",
    height=180,
    placeholder="Paste or type an email here..."
)

# ------------------------------------------------
# Run Agent
# ------------------------------------------------
if st.button("🚀 Run Agent") and not st.session_state.paused:

    st.session_state.email_text = email_text
    st.info("🔍 Analyzing email content...")
    time.sleep(1)

    email_type = analyze_email_context(email_text)

    if email_type == "empty":
        st.info("🟡 EDGE CASE: Empty Email")
        st.write("🧠 Triage Decision: **IGNORE**")

    elif email_type == "irrelevant":
        st.info("🟡 NON-WORK EMAIL")
        st.write("🧠 Triage Decision: **IGNORE**")
        st.write("📭 Casual or non-actionable content.")

    elif email_type == "ambiguous":
        st.session_state.paused = True
        st.error("⏸ AGENT PAUSED – HUMAN REVIEW REQUIRED")
        st.warning("⚠️ Ambiguous Email Detected")
        st.code(email_text)

    else:
        decision = run_email_agent(email_text)

        if decision == "respond":
            st.success("✅ SAFE EMAIL")
            st.write("✉️ Response sent automatically.")

        elif decision == "ignore":
            st.info("🟡 SAFE EMAIL")
            st.write("📭 Email ignored.")

        elif decision == "notify_human":
            st.session_state.paused = True
            st.error("⏸ AGENT PAUSED – WAITING FOR HUMAN")

# ------------------------------------------------
# HUMAN-IN-THE-LOOP CONTROLS
# ------------------------------------------------
if st.session_state.paused:

    st.subheader("🧑‍⚖️ Human Actions Required")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅ Approve"):
            st.success("✔ Approved")
            st.session_state.paused = False
            st.session_state.edit_mode = False

    with col2:
        if st.button("❌ Deny"):
            st.error("🚫 Denied")
            st.session_state.paused = False
            st.session_state.edit_mode = False

    with col3:
        if st.button("✏️ Edit"):
            st.session_state.edit_mode = True

# ------------------------------------------------
# EDIT FLOW (WRITE TO FILE ONLY)
# ------------------------------------------------
if st.session_state.edit_mode:

    st.subheader("✏️ Edit Email Content")

    edited_text = st.text_area(
        "Modify email before sending",
        value=st.session_state.email_text,
        height=200
    )

    if st.button("📤 Send Email"):
        now = datetime.now()

        with open(EDITED_EMAIL_FILE, "a", encoding="utf-8") as f:
            f.write("\n" + "-" * 40 + "\n")
            f.write(f"DATE: {now.strftime('%d-%m-%Y')}\n")
            f.write(f"TIME: {now.strftime('%I:%M:%S %p')}\n")
            f.write("STATUS: EDITED\n\n")
            f.write("ORIGINAL EMAIL:\n")
            f.write(st.session_state.email_text + "\n\n")
            f.write("EDITED EMAIL:\n")
            f.write(edited_text + "\n")
            f.write("-" * 40 + "\n")

        st.success("📨 Edited Email Sent Successfully")

        st.session_state.edit_mode = False
        st.session_state.paused = False
