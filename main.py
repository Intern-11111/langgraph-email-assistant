import os
from dotenv import load_dotenv
from openai import OpenAI

# -------------------------------------------------
# Setup
# -------------------------------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------------------------
# TRIAGE FUNCTION
# -------------------------------------------------
def triage_email(subject: str, body: str) -> dict:
    """
    Classify the email and assign priority
    """
    prompt = f"""
You are an email triage assistant.

Classify the email into ONE category:
- Interview
- Support
- Complaint
- Promotion
- Spam
- General

Also assign priority: High, Medium, Low.

Respond ONLY in JSON format:
{{
  "category": "...",
  "priority": "...",
  "reason": "short explanation"
}}

Email:
Subject: {subject}
Body: {body}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return eval(response.choices[0].message.content)


# -------------------------------------------------
# REACT FUNCTION
# -------------------------------------------------
def react_to_email(triage_result: dict) -> str:
    """
    Decide action based on category & priority
    """
    category = triage_result["category"]
    priority = triage_result["priority"]

    if category == "Interview" and priority == "High":
        return "📅 Schedule interview and notify candidate"

    if category == "Support":
        return "🛠️ Create support ticket"

    if category == "Complaint":
        return "⚠️ Escalate to manager"

    if category == "Promotion" or category == "Spam":
        return "🗑️ Ignore / Archive email"

    return "📥 Add to general inbox"


# -------------------------------------------------
# MAIN LOOP (TRIAGE → REACT)
# -------------------------------------------------
def main():
    subject = "Interview Invitation for Software Engineer Role"
    body = "We would like to schedule your interview tomorrow at 10 AM."

    print("\n📧 Incoming Email")
    print("Subject:", subject)
    print("Body:", body)

    triage = triage_email(subject, body)

    print("\n🧠 TRIAGE RESULT")
    print(triage)

    action = react_to_email(triage)

    print("\n⚡ REACT ACTION")
    print(action)


# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":
    main()
