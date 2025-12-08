import re
from openai import OpenAI

client = OpenAI()

def rule_based_triage(email_text):
    text = email_text.lower()

    spam_words = ["win", "prize", "reward", "cash", "urgent", "compromised", "refund"]
    promo_words = ["discount", "offer", "sale", "deal", "free", "%", "voucher"]
    action_words = ["schedule", "meeting", "call", "book", "approve", "send", "resolve"]

    if any(w in text for w in spam_words):
        return "spam"

    if any(w in text for w in promo_words):
        return "promotion"

    if any(w in text for w in action_words):
        return "action_intent"

    return "unknown"


def llm_fallback(email_text):
    prompt = f"Classify: spam, promotion, normal, action_intent.\nEmail: {email_text}\nOnly return label."

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content.strip().lower()
    except:
        return "normal"


def triage_email(email_text):
    rule_label = rule_based_triage(email_text)
    if rule_label != "unknown":
        return rule_label

    return llm_fallback(email_text)