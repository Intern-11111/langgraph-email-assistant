# Frontend App - Based on Payal's HITL App (Milestone 4)
# Simplified for read_calendar and send_mail tools only

import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Email Assistant - HITL",
    page_icon="📧",
    layout="centered"
)

st.title("📧 Email Assistant - HITL Mode")
st.caption("Milestone 4: Persistent Memory & HITL Workflow")

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Initialize session state
if "state" not in st.session_state:
    st.session_state.state = None
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "email-hitl-thread"
if "form_key" not in st.session_state:
    st.session_state.form_key = 0

#=== Sidebar ===
with st.sidebar:
    st.header("ℹ️ About")
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

#=== Main Interface ===
st.header("Process Email")

# Email Input Form
with st.form(key=f"email_form_{st.session_state.form_key}"):
    subject = st.text_input("Email Subject", placeholder="Meeting request...")
    body = st.text_area(
        "Email Body",
        placeholder="Can we meet next Tuesday at 2 PM?",
        height=100
    )
    submit = st.form_submit_button("🚀 Run Agent", use_container_width=True)

if submit and subject and body:
    with st.spinner("Processing email..."):
        try:
            # Send to backend
            response = requests.post(
                f"{BACKEND_URL}/v1/process-email",
                json={
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
            st.error("❌ Cannot connect to backend. Start it with:\n\n`uvicorn backend.src.main:app --port 8000`")
        except Exception as e:
            st.error(f"Error: {str(e)}")

#=== HITL Approval UI ===
if st.session_state.state:
    result = st.session_state.state
    
    #--- Waiting for HITL Approval ---
    if result.get("hitl_required"):
        st.warning("⏸️ **Human Approval Required**")
        
        action = result.get("proposed_action", {})
        tool = action.get("tool")
        args = action.get("args", {})
        
        # Show what the agent wants to do
        st.markdown("### 🤖 Agent Proposal:")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Tool", tool)
        with col2:
            st.json(args)
        
        # Preview message if send_mail
        if tool == "send_mail":
            st.markdown("### 📧 Draft Email:")
            with st.container(border=True):
                st.markdown(f"**To:** {args.get('to', 'N/A')}")
                st.markdown(f"**Subject:** {args.get('subject', 'N/A')}")
                st.markdown("**Body:**")
                st.text(args.get('body', 'N/A'))
        
        st.divider()
        
        # HITL Decision Buttons
        col_approve, col_edit, col_deny = st.columns(3)
        
        with col_approve:
            if st.button("✅ Approve", use_container_width=True, type="primary"):
                # Send approval to backend
                response = requests.post(
                    f"{BACKEND_URL}/v1/hitl-decision",
                    json={
                        "thread_id": st.session_state.thread_id,
                        "decision": "approve"
                    }
                )
                if response.status_code == 200:
                    st.session_state.state = response.json()
                    st.rerun()
        
        with col_edit:
            with st.popover("✏️ Edit"):
                if tool == "send_mail":
                    edited_body = st.text_area(
                        "Edit Message",
                        value=args.get('body', ''),
                        height=150
                    )
                    if st.button("💾 Save & Send"):
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
                            st.rerun()
                else:
                    st.info("Edit not available for this tool")
        
        with col_deny:
            if st.button("❌ Deny", use_container_width=True):
                response = requests.post(
                    f"{BACKEND_URL}/v1/hitl-decision",
                    json={
                        "thread_id": st.session_state.thread_id,
                        "decision": "deny"
                    }
                )
                if response.status_code == 200:
                    st.session_state.state = response.json()
                    st.rerun()
    
    #--- Final Result UI ---
    else:
        status = result.get("status")
        
        if status == "completed":
            st.success("✅ **Workflow Completed**")
            
            # Show tool result if exists
            if result.get("tool_result"):
                st.markdown("### 🛠️ Tool Execution Result:")
                st.json(result["tool_result"])
            
            # Show final reply if exists
            if result.get("final_reply"):
                st.markdown("### 💬 Agent Response:")
                st.info(result["final_reply"])
        
        elif status == "denied":
            st.error("❌ **Action Denied**")
            st.info("Email marked as read. No action taken.")
        
        elif status == "ignored":
            st.info("📭 **Email Ignored**")
            st.caption("Classified as newsletter/promotion")
        
        elif status == "notify_human":
            st.warning("🔔 **Flagged for Human Review**")
            st.caption("Important email - requires manual attention")
        
        else:
            st.success("✅ **Processing Complete**")
        
        # Reset button
        if st.button("🔄 Process Another Email", use_container_width=True):
            st.session_state.state = None
            st.session_state.form_key += 1  # Change form key to reset inputs
            st.rerun()
            

# Footer
st.divider()
st.caption("🧠 Milestone 4: Persistent Memory & HITL | Team A1")