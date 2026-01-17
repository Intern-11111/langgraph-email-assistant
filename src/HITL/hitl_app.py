import streamlit as st
from hitl_graph import build_graph
from db import save_email

st.set_page_config(page_title="Email Assistant HITL", layout="centered")
st.title("Email Assistant")

app = build_graph()
THREAD_ID = "email-hitl-thread"

if "state" not in st.session_state:
    st.session_state.state = None


with st.form("email_form"):
    subject = st.text_input("Email Subject")
    body = st.text_area("Email Body")
    submit = st.form_submit_button("Run Agent")

if submit:
    email_id = save_email(subject, body)
    st.session_state.state = {
        "email_text": {"subject": subject, "body": body},
        "email_id": email_id,
    }


if st.session_state.state:
    result = app.invoke(
        st.session_state.state,
        config={"configurable": {"thread_id": THREAD_ID}},
    )

    # ⏸ HITL UI
    if result.get("hitl"):
        st.warning("⚠️ Human approval required")
        st.json(result["hitl"]["action_input"])

        if st.button("✅ Approve"):
            result.pop("hitl")
            result["human_decision"] = {"action": "approve"}
            st.session_state.state = result
            st.rerun()

        edited = st.text_area(
            "Edit message",
            value=result["hitl"]["action_input"].get("message", ""),
        )
        if st.button("💾 Edit & Send"):
            result.pop("hitl")
            result["human_decision"] = {
                "action": "edit",
                "edited_args": {"message": edited},
            }
            st.session_state.state = result
            st.rerun()

        if st.button("❌ Deny"):
            result.pop("hitl")
            result["human_decision"] = {"action": "deny"}
            st.session_state.state = result
            st.rerun()

    # ✅ FINAL UI
    else:
        if result.get("status") == "IGNORED":
            st.info("📭 Email ignored")

        elif result.get("status") == "NOTIFY_HUMAN":
            st.warning("👤 Human notified")

        elif result.get("tool_result") is not None:
            st.success("🛠 Tool executed")
            st.json(result["tool_result"])

        else:
            st.success("✅ Execution completed")

        st.session_state.state = None
