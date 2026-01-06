import streamlit as st
import sys
import os

# ------------------------------------------------
# Allow importing agent logic from src/
# ------------------------------------------------
sys.path.append(os.path.abspath("src"))

from agent import run_email_agent   # must return: respond / ignore / notify_human

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(
    page_title="LangGraph Email Assistant",
    layout="centered"
)
st.title("📧 LangGraph Email Assistant")
st.write("Human-in-the-Loop UI for email triage (E1 Milestone)")

email_text = st.text_area(
    "✉️ Enter Email Content",
    height=180,
    placeholder="Paste or type an email here..."
)

if st.button("🚀 Run Agent"):
    if email_text.strip() == "":
        st.warning("Please enter an email before running the agent.")
    else:
        try:
            decision = run_email_agent(email_text)

            st.subheader("🧠 Agent Decision")

            if decision == "respond":
                st.success("✅ ACTION: RESPOND")
                st.write("The agent suggests replying to this email.")

            elif decision == "ignore":
                st.info("🟡 ACTION: IGNORE")
                st.write("The agent suggests ignoring this email.")

            elif decision == "notify_human":
                st.error("🔴 ACTION: NOTIFY HUMAN")
                st.write("This email requires immediate human attention.")

            else:
                st.warning("⚠️ Unknown output from agent")
                st.code(decision)

        except Exception as e:
            st.error("❌ Agent Execution Failed")
            st.code(str(e))
