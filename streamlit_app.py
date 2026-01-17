import streamlit as st
from src.graph.graph_registry import get_graph
from src.state.thread_registry import THREAD_REGISTRY

# --------------------------------------------------
# App setup
# --------------------------------------------------
st.set_page_config(
    page_title="HITL Email Control Center",
    page_icon="📬",
    layout="wide",
)

st.title("📬 HITL Email Control Center")
st.caption("Human-in-the-Loop Dashboard for Autonomous Email Agent")

graph = get_graph()

# --------------------------------------------------
# Load paused HITL threads (SAFE + CORRECT)
# --------------------------------------------------
st.subheader("🕒 Pending Human Decisions")

paused_threads = []

for thread_id in list(THREAD_REGISTRY):
    try:
        history = list(
            graph.get_state_history(
                config={"configurable": {"thread_id": thread_id}}
            )
        )
    except Exception:
        continue

    if not history:
        continue

    # Walk newest → oldest
    for snapshot in reversed(history):
        state = snapshot.values or {}

        if state.get("hitl_required") and state.get("human_decision") is None:
            paused_threads.append(
                {
                    "thread_id": thread_id,
                    "state": state,
                }
            )
            break  # only need latest pause

if not paused_threads:
    st.success("✅ No pending approvals. System is idle.")
    st.stop()

# --------------------------------------------------
# Thread selector
# --------------------------------------------------
thread_ids = [t["thread_id"] for t in paused_threads]

selected_thread = st.selectbox(
    "Select a paused thread",
    thread_ids,
)

selected = next(t for t in paused_threads if t["thread_id"] == selected_thread)
state = selected["state"]

st.divider()

# --------------------------------------------------
# Email context
# --------------------------------------------------
st.subheader("📨 Incoming Email")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**From**")
    st.code(state.get("from_email", "unknown"))

with col2:
    st.markdown("**Subject**")
    st.code(state.get("subject", "(no subject)"))

st.markdown("**Email Body**")
st.text_area(
    label="",
    value=state.get("email_content", ""),
    height=180,
    disabled=True,
)

# --------------------------------------------------
# Agent draft
# --------------------------------------------------
st.divider()
st.subheader("🤖 Agent Draft Reply")

st.text_area(
    label="Draft reply",
    value=state.get("draft_reply", ""),
    height=150,
    disabled=True,
)

# --------------------------------------------------
# Timeline-style execution logs
# --------------------------------------------------
st.divider()
st.subheader("🧭 Agent Execution Timeline")

logs = state.get("execution_logs", [])

if not logs:
    st.info("No execution logs available.")
else:
    for i, line in enumerate(logs, start=1):
        st.markdown(
            f"""
            <div style="
                border-left: 4px solid #22c55e;
                padding-left: 12px;
                margin-bottom: 10px;
                background-color: #020617;
                border-radius: 6px;
                padding: 10px;
            ">
                <b>Step {i}</b><br/>
                <code>{line}</code>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --------------------------------------------------
# HITL controls
# --------------------------------------------------
st.divider()
st.subheader("🧑‍⚖️ Human Decision")

decision = st.radio(
    "Choose action",
    ["approve", "edit", "deny"],
    horizontal=True,
)

edited_reply = None
if decision == "edit":
    edited_reply = st.text_area(
        "Edit reply before sending",
        value=state.get("draft_reply", ""),
        height=150,
    )

if st.button("🚀 Submit Decision", type="primary"):
    graph.update_state(
        config={"configurable": {"thread_id": selected_thread}},
        values={
            "human_decision": decision,
            "edited_reply": edited_reply if decision == "edit" else None,
            "hitl_required": False,
        },
    )

    # Resume execution from HITL gate
    graph.invoke(
        None,
        config={"configurable": {"thread_id": selected_thread}},
    )

    st.success("✅ Decision applied and graph resumed")
    st.rerun()
