import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Email Assistant - HITL",
    layout="centered"
)

st.title("Email Assistant - HITL Mode")
st.caption("Milestone 4: Persistent Memory & HITL Workflow")

BACKEND_URL = "http://localhost:8000"

# Keep track of the conversation state and form across reloads
if "state" not in st.session_state:
    st.session_state.state = None
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "email-hitl-thread"
if "form_key" not in st.session_state:
    st.session_state.form_key = 0
with st.sidebar:
    st.header("About")
    st.markdown("""
    **Tools Available:**
    - `read_calendar` - View scheduled events
    - `send_mail` - Send email response
    
    **HITL Workflow:**
    1. Enter email
    2. Agent proposes action
    3. **You review & approve**
    4. Action executes
    """)
    
    st.divider()
    st.markdown("**Team Members:**")
    st.text("• Payal")
    st.text("• Samruddhi")
    st.text("• Ganesh")
    st.text("• Aayush")

st.header("Process Email")

with st.form(key=f"email_form_{st.session_state.form_key}"):
    sender = st.text_input(
        "From (Sender Email)", 
        value="user@gmail.com",
        placeholder="sender@gamil.com"
    )
    subject = st.text_input("Email Subject", placeholder="Meeting request...")
    body = st.text_area(
        "Email Body",
        placeholder="Can we meet next Tuesday at 2 PM?",
        height=100
    )
    submit = st.form_submit_button("Run Agent", use_container_width=True)

if submit and sender and subject and body:
    with st.spinner("Processing email..."):
        try:
            # Send the email data to the backend for processing
            response = requests.post(
                f"{BACKEND_URL}/v1/process-email",
                json={
                    "sender": sender,
                    "subject": subject,
                    "body": body,
                    "thread_id": st.session_state.thread_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                st.session_state.state = response.json()
                st.rerun()
            else:
                st.error(f"Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend. Start it with:\n\n`uvicorn backend.src.main:app --port 8000`")
        except Exception as e:
            st.error(f"Error: {str(e)}")
if st.session_state.state:
    result = st.session_state.state
    
    # Show triage category prominently
    triage = result.get("triage_category")
    if triage:
        # Define colors for categories
        category_colors = {
            "ignore": "blue",
            "notify-human": "orange",
            "respond-act": "green"
        }
        color = category_colors.get(triage, "gray")
        
        st.markdown(f"### Email Category: **:{color}[{triage.upper().replace('-', ' ')}]**")
        st.divider()
    
    #--- Waiting for HITL Approval ---
    if result.get("hitl_required"):
        st.warning("**Human Approval Required**")
        
        action = result.get("proposed_action", {})
        # Support both 'tool' (old) and 'action' (new) keys
        tool = action.get("tool") or action.get("action")
        args = action.get("args", {})
        
        # Show what the agent wants to do
        st.markdown("### Agent Proposal:")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Action", tool)
        with col2:
            st.json(args)
        
        st.divider()
        
        col_approve, col_edit, col_deny = st.columns(3)
        
        with col_approve:
            if st.button("Approve", use_container_width=True, type="primary"):
                # Tell the backend the user approved the action
                response = requests.post(
                    f"{BACKEND_URL}/v1/hitl-decision",
                    json={
                        "thread_id": st.session_state.thread_id,
                        "decision": "approve"
                    }
                )
                if response.status_code == 200:
                    st.session_state.state = response.json()
                    st.toast("Action Approved!")
                    st.rerun()
        
        with col_edit:
            with st.popover("Edit"):
                if tool in ["send_mail", "send_reply"]:
                    edited_body = st.text_area(
                        "Edit Message",
                        value=args.get('body', ''),
                        height=150
                    )
                    if st.button("Save & Send"):
                        response = requests.post(
                            f"{BACKEND_URL}/v1/hitl-decision",
                            json={
                                "thread_id": st.session_state.thread_id,
                                "decision": "edit",
                                "edited_args": {"body": edited_body}
                            }
                        )
                        if response.status_code == 200:
                            st.session_state.state = response.json()
                            st.toast("Changes saved and action executed!")
                            st.rerun()
                else:
                    st.info(f"Edit not available for action: {tool}")
        
        with col_deny:
            if st.button("Deny", use_container_width=True):
                response = requests.post(
                    f"{BACKEND_URL}/v1/hitl-decision",
                    json={
                        "thread_id": st.session_state.thread_id,
                        "decision": "deny"
                    }
                )
                if response.status_code == 200:
                    st.session_state.state = response.json()
                    st.toast("Action Denied.")
                    st.rerun()
    
    # Show the final result after human decision or auto-completion
    else:
        status = result.get("status")
        decision_applied = result.get("decision_applied")
        
        if decision_applied == "deny":
            st.error("**Action Denied**")
            st.info("Action was cancelled by user. No email sent/event created.")
            
        elif decision_applied == "edit":
            st.success("**Action Edited & Executed**")
            if result.get("final_reply"):
                st.markdown("### Final Response Sent:")
                st.info(result["final_reply"])
                
        elif decision_applied == "approve":
            st.success("**Action Approved & Executed**")
            if result.get("final_reply"):
                st.markdown("### Final Response Sent:")
                st.info(result["final_reply"])
                
        elif status == "completed":
            st.success("**Workflow Completed**")
            
            # Show what action was taken based on category
            if triage == "ignore":
                st.info("Email was ignored (spam/newsletter)")
            elif triage == "notify-human":
                st.warning("Email flagged for your review (important)")
            
            if result.get("tool_result"):
                st.markdown("### Tool Execution Result:")
                st.json(result["tool_result"])
            
            if result.get("final_reply") and not decision_applied:
                st.markdown("### Agent Response:")
                st.info(result["final_reply"])
        
        elif status == "error":
            st.error("**Processing Error**")
            st.warning(result.get("message", "Unknown error occurred"))
        
        else:
            st.success("**Processing Complete**")
        
        if st.button("Process Another Email", use_container_width=True):
            st.session_state.state = None
            st.session_state.form_key += 1
            st.rerun()


st.divider()
st.divider()
st.caption("Milestone 4: Persistent Memory & HITL | Team A1")