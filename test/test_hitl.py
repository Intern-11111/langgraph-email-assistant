# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import uuid
from typing import Dict, Any
from langchain_core.messages import HumanMessage
import time
from backend.src.graph import create_graph
from backend.src.hitl_handler import handle_hitl

def test_hitl_full_cycle():
    """Test HITL with real LLM triage + ReAct loop until natural HITL trigger."""
    
    # Fixed config
    config = {"configurable": {"thread_id": "hitl-test-full-1"}}
    app = create_graph()
    
    # Full email input
    dangerous_email = {
    "messages": [],
    "mail": {
        "subject": "Meeting Tue 2PM/demo",
        "body": (
            "Hi Aayush, can we do a demo meeting on Tuesday at 2PM IST? "
            "Please check your calendar and send confirmation email."
        ),
    },
}

    
    print("🚨 END-TO-END HITL TEST (real LLM)")
    print("=" * 50)
    
    # Run triage + ReAct until HITL suspends (ignore quota errors)
    try:
        app.invoke(dangerous_email, config)
        time.sleep(10)
    except Exception as e:
        print(f"⚠️ Expected quota error during triage: {e}")
    
    # Check if HITL envelope is set (from real LLM run)
    state = app.get_state(config)
    hitl = state.values.get("hitl")
    
    if not hitl or state.values.get("hitl_decision") != "pending":
        print("❌ PRODUCTION FAIL: LLM did not trigger HITL for dangerous action")
        print(f"Final state: tool_name={state.values.get('tool_name')}")
        print(f"HITL: {hitl}")
        return False
    
    if hitl and state.values.get("hitl_decision") == "pending":
        print("🎉 LLM naturally triggered HITL")
        tool_name = hitl["tool"]
        tool_args = hitl["args"]
    else:
        print("⚠️ LLM didn't trigger HITL, forcing test state")
        tool_args = {
            "to": "aayushshah90421@gmail.com",
            "subject": "Re: Presentation scheduled",
            "body": "Hi Aayush, ...",
        }
        app.update_state(
            config,
            {
                "tool_name": "send_gmail_reply",
                "tool_args": tool_args,
                "hitl": {
                    "tool": "send_gmail_reply",
                    "args": tool_args,
                    "proposed_reply": None,
                    "triage": state.values.get("triage_category"),
                },
                "hitl_decision": "pending",
            },
        )
    
    # Get user decision
    decision = input("\nHITL decision (approve/edit/deny): ").strip().lower()
    edit_values = None
    
    if decision == "edit":
        new_to = input("New 'to' (blank to keep): ").strip()
        new_subject = input("New 'subject' (blank to keep): ").strip()
        new_body = input("New 'body' (blank to keep): ").strip()
        
        edit_values = {}
        if new_to: edit_values["to"] = new_to
        if new_subject: edit_values["subject"] = new_subject
        if new_body: edit_values["body"] = new_body
    
    # Apply and resume
    print(f"\n👤 HITL: {decision.upper()}")
    if edit_values:
        print(f"Edit values: {edit_values}")
    
    handle_hitl(app, config, decision=decision, edit_values=edit_values)
    app.invoke(None, config)
    
    # Final state
    final_state = app.get_state(config)
    print("\n🏁 FINAL STATE:")
    print(f"Triage: {final_state.values.get('triage_category')}")
    print(f"Final reply: {final_state.values.get('final_reply')}")
    print(f"HITL: {final_state.values.get('hitl')}")
    print(f"HITL decision: {final_state.values.get('hitl_decision')}")
    print(f"Tool name: {final_state.values.get('tool_name')}")
    print(f"Tool args: {final_state.values.get('tool_args')}")


if __name__ == "__main__":
    test_hitl_full_cycle()

# Next production steps
# Your HITL is now ready for:

# UI integration: Replace input() with web/mobile UI that calls handle_hitl.

# Memory updates: Add memory_update logic in hitl_checkpoint for edits.

# Risk scoring: Add confidence thresholds so low‑risk emails skip HITL.

# Deployment: Gmail API polling loop → real inbox.

# Great work getting HITL solid! 🎉