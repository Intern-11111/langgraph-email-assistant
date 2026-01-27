import streamlit as st

def render_email(email_text: str):
    st.subheader("📨 Incoming Email")
    st.text_area("Email Content", email_text, height=150, disabled=True)
