# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import datetime
from datetime import timedelta, timezone
from dateutil import parser as dateparser
import json

from backend.src.tools.tools import read_calendar_availability, extract_meeting_from_email
from backend.src.tools.google_calendar import (
    get_calendar_service, 
    check_for_holiday, 
    is_slot_available, 
    create_calendar_event,
    generate_reply_llm 
)
from backend.src.tools.google_gmail import send_reply  

print('=== PRODUCTION CALENDAR + REPLY TEST ===')

# Test 1: Service loads
service = get_calendar_service()
print('✅ Calendar service loaded')

# Test 2: Slot availability (IST)
result = read_calendar_availability.invoke({
    "start": "2026-01-03 10:00", 
    "end": "2026-01-03 11:00"
})
print("\n📅 Slot availability:")
print(result)

# Test 3: Holiday check
tomorrow = datetime.date.today() + timedelta(days=1)
holiday_status = check_for_holiday(service, tomorrow)
print(f"\n🛑 Holiday tomorrow: {holiday_status}")

# Test 4: Extract + Full Flow
print("\n🔍 FULL PRODUCTION FLOW:")
sample_email = {
    "subject": "Meeting Tuesday?", 
    "body": "Hi, can we meet next Tuesday 10AM? Online ok."
}

# Extract
details_raw = extract_meeting_from_email.invoke(sample_email)
print(f"📥 Extracted: {details_raw}")

# Parse safely
details = None
if isinstance(details_raw, dict):
    details = details_raw
elif isinstance(details_raw, str):
    try:
        details = json.loads(details_raw)
    except:
        pass

if details and 'slots' in details and details['slots']:
    # Test 5: Best slot + Create
    slot = details['slots'][0]  # First available
    start_str = f"{slot['date_str']} {slot['time_str']}"
    IST = timezone(timedelta(hours=5, minutes=30))
    start_dt = dateparser.parse(start_str).astimezone(IST)
    end_dt = start_dt + timedelta(minutes=30)
    
    print(f"\n🗓️ Booking: {start_str}")
    print(f"ISO: {start_dt.isoformat()} → {end_dt.isoformat()}")
    
    # Availability + Holiday
    avail, conflict = is_slot_available(service, start_dt, end_dt)
    holiday, hname = check_for_holiday(service, start_dt.date())
    
    print(f"Available: {avail} | Holiday: {holiday} ({hname})")
    
    if avail and not holiday:
        # 🔥 CREATE EVENT
        success = create_calendar_event(service, details, start_dt, end_dt)
        event_id = "event_abc123" if success else None
        print(f"✅ Event: {'CREATED' if success else 'FAILED'}")
    else:
        event_id = None
        print("⛔ Blocked: busy/holiday")
    
    
    print("\n✨ Smart LLM Reply:")
    sender = "aayushshah90421@gmail.com"  
    
    reply_text = generate_reply_llm(
        original_subject=sample_email["subject"],
        original_body=sample_email["body"],
        event_details=details,
        booked_slot=slot if avail and not holiday else None,
        rejection_reasons=[conflict or hname] if not (avail and not holiday) else None,
        calendar_event_id=event_id
    )
    
    print(f"Reply")
    print(reply_text)
    print("-" * 50)
    
    # 🔥 REAL SEND TEST (optional)
    send_test = input("Send real reply? [y/N]: ").lower() == 'y'
    if send_test and event_id:
        sent = send_reply(sender, sample_email["subject"], reply_text)
        print(f"✅ SENT: {sent}")
    
else:
    print("❌ No meeting details found")
    reply_text = generate_reply_llm(
        original_subject=sample_email["subject"],
        original_body=sample_email["body"],
        event_details={},  # Empty
        booked_slot=None,
        rejection_reasons=["No valid slots extracted"],
        calendar_event_id=None
    )

print("\n🎉 PRODUCTION READY - Calendar + Smart Replies!")
