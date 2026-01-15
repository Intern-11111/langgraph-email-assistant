# src/mock_tools.py

def mock_send_email():
    print("📧 [MOCK ACTION] Email reply sent successfully.")

def mock_ignore_email():
    print("🟡 [MOCK ACTION] Email ignored safely.")

def mock_sensitive_action(action: str):
    print("🔐 [MOCK SENSITIVE ACTION]")
    print(f"Simulated execution of sensitive request: {action}")

def mock_deny_action():
    print("❌ [MOCK ACTION] Human denied the request. No action taken.")
