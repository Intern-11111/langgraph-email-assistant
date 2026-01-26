"""
Test script to verify LLM removal and template-based responses.
Run this to test the new keyword-based categorization and template generation.
"""
import requests
import json

# API endpoint
API_URL = "http://localhost:8000"

# Test emails covering different categories
test_emails = [
    {
        "name": "Meeting Request",
        "email": {
            "sender": "john@example.com",
            "subject": "Can we schedule a meeting?",
            "body": "Hi, I'd like to schedule a meeting to discuss the project. Are you available next week?"
        },
        "expected_category": "respond-act"
    },
    {
        "name": "Newsletter",
        "email": {
            "sender": "newsletter@company.com",
            "subject": "Weekly Newsletter - June 2024",
            "body": "Unsubscribe here if you don't want to receive these emails."
        },
        "expected_category": "ignore"
    },
    {
        "name": "Urgent Issue",
        "email": {
            "sender": "boss@company.com",
            "subject": "URGENT: Server Down",
            "body": "Emergency! The production server is down and clients can't access the system."
        },
        "expected_category": "notify-human"
    },
    {
        "name": "Question",
        "email": {
            "sender": "colleague@company.com",
            "subject": "Question about the API",
            "body": "Can you clarify how the authentication works in the new API?"
        },
        "expected_category": "respond-act"
    },
    {
        "name": "Thank You",
        "email": {
            "sender": "client@example.com",
            "subject": "Thanks for your help!",
            "body": "Thank you so much for your assistance with the project. Really appreciate it!"
        },
        "expected_category": "respond-act"
    }
]


def test_api_health():
    """Test API health endpoint."""
    print("=" * 60)
    print("Testing API Health...")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is running")
            print(f"   Version: {data.get('version')}")
            print(f"   Features: {', '.join(data.get('features', []))}")
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return False


def test_email_processing():
    """Test email processing with different categories."""
    print("\n" + "=" * 60)
    print("Testing Email Processing (No LLM - Templates Only)")
    print("=" * 60)
    
    results = []
    
    for test in test_emails:
        print(f"\n📧 Test: {test['name']}")
        print(f"   From: {test['email']['sender']}")
        print(f"   Subject: {test['email']['subject']}")
        
        try:
            response = requests.post(
                f"{API_URL}/v1/process-email",
                json=test['email']
            )
            
            if response.status_code == 200:
                data = response.json()
                category = data.get('triage_category')
                status = data.get('status')
                
                # Check if category matches expected
                category_match = category == test['expected_category']
                
                print(f"   ✅ Status: {status}")
                print(f"   📋 Category: {category} {'✅' if category_match else '❌ (expected: ' + test['expected_category'] + ')'}")
                
                if data.get('hitl_required'):
                    print(f"   🛑 HITL Required: Human approval needed")
                    proposed = data.get('proposed_action', {})
                    if proposed.get('proposed_reply'):
                        print(f"   📝 Proposed Reply Preview:")
                        reply_preview = proposed['proposed_reply'][:150]
                        print(f"      {reply_preview}...")
                
                if data.get('final_reply'):
                    print(f"   ✅ Final Reply Generated: {len(data['final_reply'])} chars")
                
                results.append({
                    "test": test['name'],
                    "success": True,
                    "category_match": category_match
                })
            else:
                print(f"   ❌ Error: Status {response.status_code}")
                print(f"      {response.text}")
                results.append({
                    "test": test['name'],
                    "success": False,
                    "category_match": False
                })
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "test": test['name'],
                "success": False,
                "category_match": False
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total = len(results)
    successful = sum(1 for r in results if r['success'])
    correct_category = sum(1 for r in results if r['category_match'])
    
    print(f"Total Tests: {total}")
    print(f"Successful API Calls: {successful}/{total}")
    print(f"Correct Categorization: {correct_category}/{total}")
    
    if successful == total and correct_category == total:
        print("\n🎉 All tests passed! LLM removal successful.")
    else:
        print("\n⚠️ Some tests failed. Check output above.")


if __name__ == "__main__":
    print("\n🧪 EMAIL AGENT TEST SUITE - Template-Based (No LLM)")
    print("=" * 60)
    
    # Test API health first
    if test_api_health():
        # Run email processing tests
        test_email_processing()
    else:
        print("\n❌ Cannot run tests - API is not responding")
        print("   Make sure the server is running: uvicorn backend.src.main:app --reload")
