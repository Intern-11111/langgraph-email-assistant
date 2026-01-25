import datetime
from datetime import timedelta, timezone
from dateutil import parser as dateparser
import json

from backend.src.tools.google_gmail import (get_gmail_service, fetch_emails, send_reply, mark_as_processed, get_sender_and_subject, get_clean_body)
from backend.src.tools.google_calendar import (get_calendar_service, extract_event_details_llm, check_for_holiday, is_slot_available, 
                     book_best_slot, generate_reply_llm)

print('=== PRODUCTION AI EMAIL AGENT ===')


print('✅ Loading services...')
calendar_service = get_calendar_service()
gmail_service = get_gmail_service()
print('✅ Gmail + Calendar services loaded')

#PROCESS REAL PRIMARY UNREAD EMAILS
print("\n🔍 Scanning PRIMARY inbox...")
emails = fetch_emails()  
if not emails:
    print("✅ No unread PRIMARY emails found.")
    exit()

print(f"📥 Found {len(emails)} PRIMARY unread email(s)")

# Process FIRST unread PRIMARY email only (safety)
email = emails[0]
print(f"\n📧 Processing: {email['subject']}")
print(f"   From: {email['sender']}")
print(f"   Preview: {email['body'][:100]}...")

# 1️⃣ EXTRACT MEETING DETAILS (your LLM function)
print("\n🤖 Extracting meeting details...")
event_details = extract_event_details_llm(email['body'], email['subject'])

if not event_details or not event_details.get('slots'):
    print("❌ No meeting details found")
    reply_text = generate_reply_llm(
        original_subject=email['subject'],
        original_body=email['body'],
        event_details={},
        booked_slot=None,
        rejection_reasons=["No valid meeting details found"],
        calendar_event_id=None
    )
else:
    print(f"✅ Found: {event_details['summary']} | {len(event_details['slots'])} slot(s)")
    
    booked_successfully, booked_slot, rejection_reasons = book_best_slot(calendar_service, event_details)
    
    # 3️⃣ GENERATE SMART REPLY
    reply_text = generate_reply_llm(
        original_subject=email['subject'],
        original_body=email['body'],
        event_details=event_details,
        booked_slot=booked_slot,
        rejection_reasons=rejection_reasons if not booked_successfully else None,
        calendar_event_id="auto-generated" if booked_successfully else None
    )

print("\n✨ AI Generated Reply:")
print(reply_text)
print("-" * 60)

# 🔥 4️⃣ HUMAN APPROVAL (HITL)
send_test = input("\n✅ Approve & Send reply? [y/N]: ").strip().lower()
if send_test == 'y':
    print("📤 Sending reply...")
    
    success = send_reply(email['sender'], email['subject'], reply_text)
    
    if success:
        # MARK AS PROCESSED using YOUR production function
        mark_as_processed(email['id'])
        print("🎉 SENT & MARKED PROCESSED ✅")
    else:
        print("❌ Send failed")
else:
    print("⏸️ Skipped")

print("\n🎉 AI AGENT COMPLETE!")
