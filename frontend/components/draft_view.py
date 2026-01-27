import streamlit as st

def render_draft(draft: str):
    st.subheader("✍️ Draft Reply")
    st.text_area("Generated Draft", draft or "—", height=150)
