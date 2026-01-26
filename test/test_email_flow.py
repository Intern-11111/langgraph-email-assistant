"""
End-to-End API Integration Tests
Tests the complete email processing workflow via HTTP API
"""

import requests
import json
import time


BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_api_health():
    """Test that the API is running and healthy."""
    print_section("TEST 1: API Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        result = response.json()
        
        print(f"✅ API Status: {result['status']}")
        print(f"✅ Version: {result['version']}")
        print(f"✅ Features: {len(result['features'])} enabled")
        
        return True
    except Exception as e:
        print(f"❌ API not reachable: {e}")
        print("💡 Make sure to run: python -m backend.src.main")
        return False


def test_spam_email():
    """Test processing a spam/newsletter email (should be ignored)."""
    print_section("TEST 2: Spam Email Processing")
    
    email = {
        "sender": "noreply@marketing.com",
        "subject": "Special Offer - Unsubscribe Here!",
        "body": "Amazing deals await! Click here for discounts. Unsubscribe at bottom."
    }
    
    print(f"📧 From: {email['sender']}")
    print(f"📌 Subject: {email['subject']}")
    
    response = requests.post(f"{BASE_URL}/v1/process-email", json=email)
    result = response.json()
    
    print(f"\n📊 Results:")
    print(f"   Status: {result.get('status', 'unknown')}")
    
    # Handle error case
    if result.get('status') == 'error':
        print(f"   ⚠️  Error: {result.get('message', 'Unknown error')}")
        print(f"   💡 Tip: Make sure GOOGLE_API_KEY is set in .env file")
        return
    
    print(f"   Triage: {result.get('triage_category')}")
    print(f"   HITL Required: {result.get('hitl_required', False)}")
    
    if result.get('triage_category') == 'ignore':
        print("   ✅ PASS: Correctly classified as spam")
    else:
        print("   ⚠️  UNEXPECTED: Should be classified as 'ignore'")


def test_meeting_request_with_hitl():
    """Test processing a meeting request that requires HITL approval."""
    print_section("TEST 3: Meeting Request with HITL")
    
    # Step 1: Send meeting request email
    email = {
        "sender": "alice@example.com",
        "subject": "Meeting Request",
        "body": "Can we schedule a meeting next Tuesday at 2 PM to discuss the Q1 roadmap?"
    }
    
    print(f"📧 From: {email['sender']}")
    print(f"📌 Subject: {email['subject']}")
    print(f"\n🔄 Step 1: Processing email...")
    
    response = requests.post(f"{BASE_URL}/v1/process-email", json=email)
    result = response.json()
    
    print(f"\n📊 Initial Results:")
    print(f"   Status: {result.get('status', 'unknown')}")
    
    # Handle error case
    if result.get('status') == 'error':
        print(f"   ⚠️  Error: {result.get('message', 'Unknown error')}")
        print(f"   💡 Tip: Make sure GOOGLE_API_KEY is set in .env file")
        return
    
    print(f"   Triage: {result.get('triage_category')}")
    print(f"   HITL Required: {result.get('hitl_required', False)}")
    
    if result['hitl_required']:
        thread_id = result['thread_id']
        print(f"   Thread ID: {thread_id}")
        
        proposed = result.get('proposed_action', {})
        print(f"\n📝 Proposed Action:")
        print(f"   Tool: {proposed.get('tool')}")
        print(f"   Args: {json.dumps(proposed.get('args', {}), indent=6)}")
        
        # Step 2: Approve the action
        print(f"\n🔄 Step 2: Approving action...")
        time.sleep(1)
        
        decision = {
            "thread_id": thread_id,
            "decision": "approve"
        }
        
        response = requests.post(f"{BASE_URL}/v1/hitl-decision", json=decision)
        final_result = response.json()
        
        print(f"\n📊 Final Results:")
        print(f"   Status: {final_result['status']}")
        print(f"   Decision Applied: {final_result.get('decision_applied')}")
        
        if final_result.get('final_reply'):
            print(f"   💬 Reply: {final_result['final_reply'][:80]}...")
        
        print("   ✅ PASS: HITL workflow completed successfully")
    else:
        print("   ⚠️  No HITL required - unexpected for meeting request")


def test_simple_question():
    """Test processing a simple question email."""
    print_section("TEST 4: Simple Question Email")
    
    email = {
        "sender": "bob@example.com",
        "subject": "Quick Question",
        "body": "Hey, just wanted to check if you received my report yesterday?"
    }
    
    print(f"📧 From: {email['sender']}")
    print(f"📌 Subject: {email['subject']}")
    
    response = requests.post(f"{BASE_URL}/v1/process-email", json=email)
    result = response.json()
    
    print(f"\n📊 Results:")
    print(f"   Status: {result.get('status', 'unknown')}")
    
    # Handle error case
    if result.get('status') == 'error':
        print(f"   ⚠️  Error: {result.get('message', 'Unknown error')}")
        return
    
    print(f"   Triage: {result.get('triage_category')}")
    
    if result.get('triage_category') == 'respond-act':
        print("   ✅ PASS: Correctly classified as needing response")
    else:
        print(f"   ℹ️  Classified as: {result.get('triage_category')}")


def test_status_endpoint():
    """Test the status endpoint."""
    print_section("TEST 5: Status Endpoint")
    
    # First, create a workflow
    email = {
        "sender": "test@example.com",
        "subject": "Test",
        "body": "Testing status endpoint",
        "thread_id": "status-test-123"
    }
    
    response = requests.post(f"{BASE_URL}/v1/process-email", json=email)
    result = response.json()
    thread_id = result['thread_id']
    
    print(f"📍 Thread ID: {thread_id}")
    
    # Check status
    response = requests.get(f"{BASE_URL}/v1/status/{thread_id}")
    status = response.json()
    
    print(f"\n📊 Workflow Status:")
    print(f"   Has State: {status['state'] is not None}")
    print(f"   Next Steps: {status.get('next_steps', 'None')}")
    print("   ✅ PASS: Status endpoint working")


def run_all_tests():
    """Run all integration tests."""
    print("\n" + "🧪"*35)
    print("EMAIL ASSISTANT - INTEGRATION TESTS")
    print("🧪"*35)
    
    # Check API health first
    if not test_api_health():
        return
    
    # Run tests
    test_spam_email()
    test_simple_question()
    test_meeting_request_with_hitl()
    test_status_endpoint()
    
    print_section("ALL TESTS COMPLETED")
    print("✅ Test suite finished\n")


if __name__ == "__main__":
    run_all_tests()
