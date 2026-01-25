# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# import sys
# import os

# # Get the absolute path of the directory where 'test' folder lives
# # This should be 'D:\...\langgraph-email-assistant'
# project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# if project_root not in sys.path:
#     sys.path.insert(0, project_root)
    
import uuid
from typing import Dict, Any
from backend.src.graph import create_graph
from backend.src.hitl_handler import handle_hitl

def test_hitl_force_no_llm():
    config = {"configurable": {"thread_id": "hitl-test-force-v6"}}
    app = create_graph()
    
    print("🚨 FORCE HITL TEST (NO LLM GENERATION)")
    print("=" * 50)
    
    # 1. Define the Simulated LLM Output
    fake_tool_args = {
        "to": "sarah@example.com",
        "subject": "Re: Inquiry about pricing", 
        "body": "Hi Sarah, Q4 price list attached. Let me know if you need more details.",
    }

    # 2. Force the State
    # FIXED: Added "mail" object so triage_node doesn't crash
    forced_state = {
        "messages": [], 
        "triage_category": "respond-act", 
        "mail": {
            "subject": "Inquiry about pricing",
            "body": "Hi, can you send Q4 pricing details? Thanks! - Sarah",
            "from": "sarah@example.com"
        },
        "tool_name": "send_gmail_reply",
        "tool_args": fake_tool_args,
        "hitl": {
            "tool": "send_gmail_reply",
            "args": fake_tool_args,
            "proposed_reply": fake_tool_args["body"], 
            "triage": "respond-act",
        },
        "hitl_decision": "pending",
    }
    
    print("🛠️ Injecting mocked state...")
    # NOTE: If your graph starts at triage_node, it might still run briefly. 
    # Providing 'mail' prevents the crash.
    app.update_state(config, forced_state)
    
    # 3. Show the "Proposed" Reply
    state = app.get_state(config)
    tool_args = state.values["tool_args"]
    
    print("\n📧 PROPOSED REPLY (MOCKED):")
    print(f"  To: {tool_args['to']}")
    print(f"  Subject: {tool_args['subject']}")
    print(f"  Body: {tool_args['body']}")
    
    # 4. Get user decision
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
    
    # 5. Apply HITL logic
    print(f"\n👤 HITL: {decision.upper()}")
    if edit_values:
        print(f"Edit values: {edit_values}")
    
    handle_hitl(app, config, decision=decision, edit_values=edit_values)
    
    # 6. Resume the Graph
    print("🚀 Resuming graph execution...")
    app.invoke(None, config)
    
    # 7. Final Verification
    final_state = app.get_state(config)
    print("\n🏁 FINAL STATE:")
    print(f"Triage: {final_state.values.get('triage_category')}")
    print(f"Final reply: {final_state.values.get('final_reply')}")
    print(f"HITL decision: {final_state.values.get('hitl_decision')}")
    print(f"Tool executed: {final_state.values.get('tool_name')}")
    
    if decision == 'deny':
        print("✅ Email DENIED (Not sent)")
    else:
        print("✅ Email SENT (Tool executed)")

if __name__ == "__main__":   
    test_hitl_force_no_llm()