# Test script for Mock Mode
# Run this to verify the mock setup works

print("🧪 Testing Mock Mode Setup...")
print("=" * 50)

# Test 1: Mock Gmail
print("\n1️⃣ Testing Mock Gmail...")
try:
    from backend.src.tools.mock_gmail import fetch_emails, send_reply, mark_as_processed
    emails = fetch_emails()
    print(f"✅ Retrieved {len(emails)} mock emails")
    print(f"   First email: {emails[0]['subject']}")
    
    # Test send
    send_reply("test@example.com", "Test Subject", "Test Body")
    
    # Test mark as processed
    mark_as_processed("mock_001")
    
    print("✅ Mock Gmail working!")
except Exception as e:
    print(f"❌ Mock Gmail error: {e}")

# Test 2: Mock Calendar
print("\n2️⃣ Testing Mock Calendar...")
try:
    from backend.src.tools.mock_calendar import read_calendar, check_availability, create_calendar_event
    events = read_calendar()
    print(f"✅ Retrieved {len(events)} calendar events")
    print(f"   First event: {events[0]['title']}")
    
    # Test availability
    avail = check_availability("2026-01-28", "14:00")
    print(f"✅ Availability check: {avail}")
    
    # Test create event
    create_calendar_event("Test Meeting", "2026-01-28T14:00:00", "2026-01-28T15:00:00")
    
    print("✅ Mock Calendar working!")
except Exception as e:
    print(f"❌ Mock Calendar error: {e}")

# Test 3: Mock Contacts
print("\n3️⃣ Testing Mock Contacts...")
try:
    from backend.src.tools.mock_contacts import lookup_contact, get_all_contacts
    contact = lookup_contact("alice")
    print(f"✅ Found contact: {contact['name']} - {contact['email']}")
    
    all_contacts = get_all_contacts()
    print(f"✅ Total contacts: {len(all_contacts)}")
    
    print("✅ Mock Contacts working!")
except Exception as e:
    print(f"❌ Mock Contacts error: {e}")

# Test 4: Backend imports
print("\n4️⃣ Testing Backend imports...")
try:
    from backend.src.config import gemini_ai_model
    from backend.src.state import AgentState  
    from backend.src.graph import create_graph
    print("✅ Backend core imports working!")
except Exception as e:
    print(f"❌ Backend import error: {e}")

# Test 5: Tools integration
print("\n5️⃣ Testing Tools integration...")
try:
    from backend.src.tools.tools import (
        send_gmail_reply, 
        read_calendar_availability,
        lookup_contact_tool,
        get_user_prefs
    )
    print("✅ All tool imports working!")
except Exception as e:
    print(f"❌ Tools integration error: {e}")

print("\n" + "=" * 50)
print("🎉 Mock Mode Setup Complete!")
print("\nNext steps:")
print("1. uvicorn backend.src.main:app --reload --port 8000")
print("2. streamlit run frontend/app.py --server.port 8501")
print("3. Open http://localhost:8501")
print("4. Click 'Scan Mock Inbox'")
