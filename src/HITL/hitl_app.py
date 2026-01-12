import streamlit as st
from hitl_graph import build_graph
from db import save_email, get_email

st.set_page_config(page_title="Email Assistant HITL", layout="centered")
st.title("Email Assistant")

app = build_graph()
THREAD_ID = "email-hitl-thread"

# -------------------------------
# Session state
# -------------------------------
if "state" not in st.session_state:
    st.session_state.state = None

# -------------------------------
# Email input
# -------------------------------
with st.form("email_form"):
    subject = st.text_input("Email Subject")
    body = st.text_area("Email Body")
    submit = st.form_submit_button("Run Agent")

if submit:
    email_id = save_email(subject, body)
    st.session_state.state = {
        "email_text": {   
            "subject": subject,
            "body": body
        },
        "email_id": email_id
    }

# -------------------------------
# Run / Resume graph
# -------------------------------
if st.session_state.state:
    result = app.invoke(
        st.session_state.state,
        config={"configurable": {"thread_id": THREAD_ID}}
    )

    # HITL PAUSE
    if "hitl" in result and result["hitl"]["status"] == "WAITING_FOR_HUMAN":
        st.warning("⚠️ Human approval required")

        st.markdown("**Proposed Action Input:**")
        st.write(result["hitl"]["action_input"])

        # Approve
        if st.button("✅ Approve"):
            result.pop("hitl", None)     
            result["human_decision"] = {"action": "approve"}
            st.session_state.state = result
            st.rerun()

        # Edit
        edited_text = st.text_area(
            "Edit reply",
            value=result["hitl"]["action_input"].get("message", "")
        )
        if st.button(" Save Edit & Send"):
            result.pop("hitl", None)     
            result["human_decision"] = {
                "action": "edit",
                "edited_args": {"message": edited_text}
            }
            st.session_state.state = result
            st.rerun()

        # Deny
        if st.button("Deny"):
            result.pop("hitl", None)     
            result["human_decision"] = {"action": "deny"}
            st.session_state.state = result
            st.rerun()

    # COMPLETED
    else:
        st.success("✅ Execution completed")
        st.write(result.get("tool_result"))
        st.session_state.state = None
