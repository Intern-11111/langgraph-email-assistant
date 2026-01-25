# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.src.tools.tools import fetch_emails,process_email,DANGEROUS_TOOLS,send_gmail_reply


print('=== GMAIL TESTS ===')
print(f'DANGEROUS_TOOLS: {DANGEROUS_TOOLS}')

# Test 1: Fetch unread emails
emails = fetch_emails()  # Default: inbox unread -trash -spam
print(f'Primary unread: {len(emails)}')
for email in emails[:2]:  # First 2
    print(f"ID: {email['id'][:8]} | {email['sender'][:30]}: {email['subject']}")


#Test 2: Process email (safe - marks read)
if emails:
    result = process_email.invoke({"msg_id":emails[0]['id']})
    print(f'Processed: {result}')


#Test 3: Send Email
TEST_TO = "aayushshah90421@gmail.com"
TEST_SUBJECT = "LangGraph Agent Test - Fixed"
TEST_BODY = """
Hi Aayush,

Ambient agent email send FIXED!
- Gmail API: ✓ Working
- Import fixed: sendgmailreplyto
- ReAct ready next

Best,
Your AI Assistant
"""

print(f"Sending to {TEST_TO}...")
result = send_gmail_reply.invoke({  # ← Correct name
    "to": TEST_TO,
    "subject": TEST_SUBJECT,
    "body": TEST_BODY
})
print(f'Result: {result}')

print('Send test complete ✓')
print('Check inbox!')
