import streamlit as st

# -----------------------------
# HITL Review UI (Milestone-1)
# -----------------------------

st.title("HITL Review Dashboard")

# Dummy data for Milestone-1
email_text = "Customer is requesting a refund for a recent purchase."
triage_decision = "Requires Human Approval (Financial Category)"
explanation = "This email involves a financial request and must be reviewed by a human."

st.subheader("Original Email")
st.write(email_text)

st.subheader("Triage Decision")
st.write(triage_decision)

st.subheader("AI Explanation")
st.write(explanation)

st.subheader("Human Action")

col1, col2 = st.columns(2)

with col1:
    if st.button("Approve"):
        st.success("Action Approved by Human")

with col2:
    if st.button("Escalate"):
        st.warning("Action Escalated for Further Review")

st.info("LangSmith will be used to log triage decisions, ReAct reasoning, and HITL approvals.")

# --------------------------------------------------
# Safety Policy (Milestone-1)
# --------------------------------------------------
# - Financial emails require mandatory human approval
# - Legal or account-related emails must be escalated
# - No automated action is taken without HITL approval

