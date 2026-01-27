import streamlit as st

def render_hitl_controls(draft: str):
    st.warning("⚠️ Human approval required before execution")

    decision = None
    edited_reply = None

    st.markdown("### ✍️ Optional Edit (for *Edit* decision)")
    edited_reply = st.text_area(
        "Edit the draft before approving",
        value=draft,
        height=150,
        key="edited_reply",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        approve = st.button("✅ Approve")
    with col2:
        deny = st.button("❌ Deny")
    with col3:
        edit = st.button("✏️ Edit & Approve")

    if approve:
        decision = "approve"
    elif deny:
        decision = "deny"
    elif edit:
        decision = "edit"

    return decision, edited_reply
