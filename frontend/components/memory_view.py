import streamlit as st

def render_memory(memory: dict):
    st.subheader("🧠 Memory Used")
    if not memory:
        st.info("No memory injected")
    else:
        st.json(memory)
