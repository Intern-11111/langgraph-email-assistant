import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from run_backend import run_agent


st.set_page_config(page_title="LangGraph Email Assistant", layout="centered")

st.title("📧 LangGraph Email Assistant")
st.write("An end-to-end Email Agent with Human-in-the-Loop safety")

# Email input
subject = st.text_input("Email Subject")
body = st.text_area("Email Body")

if "agent_state" not in st.session_state:
    st.session_state.agent_state = None

if st.button("Run Agent"):
    result = run_agent(subject, body)
    st.session_state.agent_state = result

# Show agent output
if st.session_state.agent_state:
    state = st.session_state.agent_state

    st.subheader("🔍 Agent Decision")
    st.write(state.get("triage_decision"))

    st.subheader("🧠 Draft Response")
    st.write(state.get("draft_response"))

    # If paused, show approval buttons
    if state.get("paused", False):
        st.warning("⚠️ Human approval required")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("✅ Approve"):
                updated = run_agent(subject, body, user_action="approve")
                st.session_state.agent_state = updated

        with col2:
            if st.button("❌ Deny"):
                updated = run_agent(subject, body, user_action="deny")
                st.session_state.agent_state = updated

        with col3:
            edited_text = st.text_input("✏️ Edit draft")
            if st.button("✏️ Submit Edit"):
                updated = run_agent(
                    subject,
                    body,
                    user_action="edit",
                    edited_text=edited_text
                )
                st.session_state.agent_state = updated

    # Final status
    if state.get("tool_status") == "blocked":
        st.error("🚫 Dangerous action blocked until confirmation")
