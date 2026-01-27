# import streamlit as st

# from api_client import (
#     triage_email,
#     submit_hitl_decision,
#     list_hitl_threads,
#     get_thread_logs,
# )
# from demo_data import DEMO_EMAILS
# from state_adapter import extract_ui_state

# from components.email_view import render_email
# from components.draft_view import render_draft
# from components.hitl_controls import render_hitl_controls
# from components.logs_view import render_logs
# from components.memory_view import render_memory

# # --------------------------------------------------
# # PAGE CONFIG
# # --------------------------------------------------
# st.set_page_config(page_title="Ambient Email Agent", layout="wide")
# st.title("📌 Ambient Email Agent – Demo")

# # --------------------------------------------------
# # EMAIL SELECTION
# # --------------------------------------------------
# email_titles = [e["title"] for e in DEMO_EMAILS]
# selected = st.selectbox("Choose Demo Email", email_titles)

# email_obj = next(e for e in DEMO_EMAILS if e["title"] == selected)
# email_text = email_obj["content"]

# # --------------------------------------------------
# # RUN AGENT
# # --------------------------------------------------
# if st.button("▶️ Run Agent"):
#     with st.spinner("Running LangGraph..."):
#         triage_email(email_text)

#         hitl_data = list_hitl_threads()
#         paused_threads = hitl_data.get("paused_threads", [])

#         if not paused_threads:
#             st.info("No HITL required for this email.")
#             st.session_state.pop("backend_state", None)
#             st.session_state.pop("thread_id", None)
#         else:
#             # Always pick MOST RECENT paused thread
#             active_thread = paused_threads[-1]
#             thread_id = active_thread["thread_id"]

#             logs_resp = get_thread_logs(thread_id)

#             ui_state = extract_ui_state(
#                 active_thread,
#                 logs_resp.get("execution_logs", []),
#             )

#             st.session_state.backend_state = ui_state
#             st.session_state.thread_id = thread_id

# # --------------------------------------------------
# # RENDER UI
# # --------------------------------------------------
# if "backend_state" in st.session_state:
#     ui_state = st.session_state.backend_state

#     render_email(email_text)
#     render_draft(ui_state["draft"])
#     render_memory(ui_state.get("memory_used", {}))
#     render_logs(ui_state["logs"])

#     if ui_state["hitl_required"]:
#         # ⬇️ UPDATED: supports approve / deny / edit
#         decision, edited_reply = render_hitl_controls(ui_state["draft"])

#         if decision:
#             with st.spinner("Resuming graph..."):
#                 if decision == "edit":
#                     submit_hitl_decision(
#                         thread_id=st.session_state.thread_id,
#                         decision="edit",
#                         edited_reply=edited_reply,
#                     )
#                 else:
#                     submit_hitl_decision(
#                         thread_id=st.session_state.thread_id,
#                         decision=decision,
#                     )

#                 st.success(f"Decision '{decision}' submitted. Graph resumed.")

#                 # Clean only what we own
#                 st.session_state.pop("backend_state", None)
#                 st.session_state.pop("thread_id", None)

#                 st.rerun()

import time
import streamlit as st

from api_client import (
    triage_email,
    submit_hitl_decision,
    list_hitl_threads,
    get_thread_logs,
)
from demo_data import DEMO_EMAILS
from state_adapter import extract_ui_state

from components.email_view import render_email
from components.draft_view import render_draft
from components.hitl_controls import render_hitl_controls
from components.logs_view import render_logs
from components.memory_view import render_memory

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Ambient Email Agent", layout="wide")
st.title("Ambient Email Agent")

# --------------------------------------------------
# MODE SELECTOR
# --------------------------------------------------
mode = st.radio(
    "Mode",
    ["Demo", "Realtime (Gmail)"],
    horizontal=True,
)

st.divider()

# --------------------------------------------------
# DEMO MODE
# --------------------------------------------------
if mode == "Demo":
    email_titles = [e["title"] for e in DEMO_EMAILS]
    selected = st.selectbox("Choose Demo Email", email_titles)

    email_obj = next(e for e in DEMO_EMAILS if e["title"] == selected)
    email_text = email_obj["content"]

    if st.button("Run Agent"):
        with st.spinner("Running LangGraph..."):
            triage_email(email_text)

# --------------------------------------------------
# REALTIME MODE (GMAIL)
# --------------------------------------------------
if mode == "Realtime (Gmail)":
    st.info("Listening for incoming Gmail messages…")

    # Manual refresh (safe)
    if st.button("Refresh"):
        st.session_state["refresh"] = True

    # Auto-refresh toggle
    auto = st.checkbox("Auto refresh (every 3s)", value=True)

    hitl_data = list_hitl_threads()
    paused_threads = hitl_data.get("paused_threads", [])

    if not paused_threads:
        st.success("No emails awaiting human approval")
    else:
        st.warning(f"{len(paused_threads)} email(s) awaiting approval")

        for t in paused_threads:
            with st.expander(
                f"From: {t.get('from')} | Subject: {t.get('subject')}",
                expanded=True,
            ):
                thread_id = t["thread_id"]

                logs_resp = get_thread_logs(thread_id)
                ui_state = extract_ui_state(
                    t,
                    logs_resp.get("execution_logs", []),
                )

                render_draft(ui_state["draft"])
                render_logs(ui_state["logs"])

                decision, edited_reply = render_hitl_controls(ui_state["draft"])

                if decision:
                    with st.spinner("Resuming graph..."):
                        if decision == "edit":
                            submit_hitl_decision(
                                thread_id=thread_id,
                                decision="edit",
                                edited_reply=edited_reply,
                            )
                        else:
                            submit_hitl_decision(
                                thread_id=thread_id,
                                decision=decision,
                            )

                        st.success(
                            f"Decision '{decision}' submitted for thread {thread_id}"
                        )
                        st.rerun()

    # Auto-refresh logic
    if auto:
        time.sleep(3)
        st.rerun()
