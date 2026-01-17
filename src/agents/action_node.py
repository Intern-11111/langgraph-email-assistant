# from src.integrations.gmail import send_email
# from src.integrations.calendar import create_calendar_event
# from src.graph.state import EmailState


# def action_node(state: EmailState) -> EmailState:
#     print("\nACTION NODE ENTERED")

#     # ⛔ Guard: if no human decision yet, do nothing (means graph was resumed wrongly)
#     if state.human_decision is None:
#         print("BLOCKED: No human decision yet. Waiting for HITL.")
#         return state

#     # DENY
#     if state.human_decision == "deny":
#         print("ACTION DENIED — no execution")
#         return state

#     final_body = state.edited_reply if state.human_decision == "edit" else state.draft_reply

#     try:
#         if state.selected_tool == "send_email":
#             print("Executing Gmail API...")
#             send_email(
#                 to=state.tool_payload.get("to", "example@gmail.com"),
#                 subject=state.tool_payload.get("subject", "Automated Reply"),
#                 body=final_body,
#             )
#             print("EMAIL SENT SUCCESSFULLY ✅")

#         elif state.selected_tool == "create_calendar_event":
#             print("Executing Calendar API...")
#             create_calendar_event(
#                 title=state.tool_payload.get("title", "Meeting"),
#                 start_time=state.tool_payload.get("start_time"),
#                 end_time=state.tool_payload.get("end_time"),
#                 description=final_body,
#             )
#             print("CALENDAR EVENT CREATED ✅")

#         else:
#             print("UNKNOWN TOOL — no execution")

#     except Exception as e:
#         print("ACTION FAILED:", str(e))

#     return state



