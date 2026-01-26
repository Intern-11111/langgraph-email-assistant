"""
Standalone Email Agent Runner
Processes mock emails through the LangGraph workflow
"""

from backend.src.graph import create_graph
from langgraph.checkpoint.memory import MemorySaver
from backend.src.tools.mock_gmail import fetch_emails
import json


def main():
    """Run the email agent with mock emails."""
    print("\n" + "="*70)
    print("EMAIL ASSISTANT - STANDALONE MODE")
    print("="*70)
    
    # Create graph with memory persistence
    memory = MemorySaver()
    graph = create_graph(checkpointer=memory)
    print("✅ Graph initialized with MemorySaver")
    
    # Fetch mock emails
    emails = fetch_emails()
    print(f"✅ Fetched {len(emails)} mock emails\n")
    
    for idx, email in enumerate(emails, 1):
        print(f"\n{'─'*70}")
        print(f"Processing Email {idx}/{len(emails)}")
        print(f"{'─'*70}")
        print(f"📧 From: {email['sender']}")
        print(f"📌 Subject: {email['subject']}")
        print(f"📄 Body: {email['body'][:60]}...")
        
        # Create initial state
        state = {
            "mail": email,
            "userid": "test_user",
            "messages": [],
            "triage_category": None,
            "tool_name": None,
            "tool_args": None,
            "final_reply": None,
            "hitl": None,
            "hitl_decision": None
        }
        
        # Process email through graph
        config = {"configurable": {"thread_id": email["id"]}}
        
        try:
            result = graph.invoke(state, config=config)
            
            print(f"\n📊 Results:")
            print(f"   Triage Category: {result.get('triage_category')}")
            
            if result.get('hitl_decision') == 'pending':
                print(f"   ⏸️  Status: Paused at HITL checkpoint")
                print(f"   🔧 Tool: {result.get('hitl', {}).get('tool')}")
                print(f"   📝 Args: {json.dumps(result.get('hitl', {}).get('args', {}), indent=6)}")
            elif result.get('final_reply'):
                print(f"   ✅ Status: Completed")
                print(f"   💬 Reply: {result['final_reply'][:100]}...")
            else:
                print(f"   ℹ️  Status: Processed (no reply)")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print(f"\n{'='*70}")
    print("PROCESSING COMPLETE")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
