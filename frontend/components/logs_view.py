import streamlit as st

def render_logs(logs):
    st.subheader("🧾 Execution Logs")
    for log in logs:
        st.code(log)
