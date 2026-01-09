import streamlit as st
import sys
import os
import time

# ------------------------------------------------
# Import agent logic
# ------------------------------------------------
sys.path.append(os.path.abspath("src"))
from agent import run_email_agent   # returns: respond / ignore / notify_human

# ------------------------------------------------
# Page Config
# ------------------------------------------------
st.set_page_config(page_title="LangGraph Email Assistant", layout="centered")
st.title("📧 LangGraph Email Assistant")
st.write("Human-in-the-Loop Email Triage (Milestone 3)")

# ------------------------------------------------
# Session State
# ------------------------------------------------
if "paused" not in st.session_state:
    st.session_state.paused = False

if "decision" not in st.session_state:
    st.session_state.decision = None

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
# Run Agent Button
# ------------------------------------------------
if st.button("🚀 Run Agent") and not st.session_state.paused:

    if email_text.strip() == "":
        st.warning("Please enter an email before running the agent.")
    else:
        st.session_state.email_text = email_text

        # 🔍 Verification message (always shown)
        st.info("🔍 Verifying whether the email is safe or dangerous...")
        time.sleep(1.5)

        decision = run_email_agent(email_text)
        st.session_state.decision = decision

        # ---------------- SAFE EMAIL ----------------
        if decision == "respond":
            st.success("✅ SAFE EMAIL")
            st.write("🧠 Agent Decision: RESPOND")
            st.write("✉️ Response sent automatically.")

        elif decision == "ignore":
            st.info("🟡 SAFE EMAIL")
            st.write("🧠 Agent Decision: IGNORE")
            st.write("📭 Email ignored.")

        # ---------------- DANGEROUS EMAIL ----------------
        elif decision == "notify_human":
            st.session_state.paused = True
            st.error("⏸ AGENT PAUSED – WAITING FOR HUMAN ACTION")
            st.warning("🔔 Notifying human for approval")

        else:
            st.warning("⚠️ Unknown agent output")
            st.code(decision)

# ------------------------------------------------
# HUMAN-IN-THE-LOOP CONTROLS (ONLY FOR DANGEROUS)
# ------------------------------------------------
if st.session_state.paused:

    st.subheader("🧑‍⚖️ Human Actions Required")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅ Approve"):
            st.success("✔ Email Approved by Human")
            st.write("✉️ Agent resumed and response sent.")
            st.session_state.paused = False

    with col2:
        if st.button("❌ Deny"):
            st.error("🚫 Email Denied by Human")
            st.write("No action taken.")
            st.session_state.paused = False

    with col3:
        if st.button("✏️ Edit"):
            st.session_state.edit_mode = True

# ------------------------------------------------
# EDIT FLOW
# ------------------------------------------------
if st.session_state.edit_mode:

    st.subheader("✏️ Edit Email Content")

    edited_text = st.text_area(
        "Modify email before sending",
        value=st.session_state.email_text,
        height=200
    )

    if st.button("📤 Send Email"):
        st.success("📨 Edited Email Sent Successfully")
        st.session_state.edit_mode = False
        st.session_state.paused = False
