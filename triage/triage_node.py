import re
from typing import TypedDict
from openai import OpenAI

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

client = OpenAI()

LABELS = ["spam", "promotion", "normal", "action_intent", "unknown"]

# tools that can change real-world state
DANGEROUS_TOOLS = {
    "send_email": "sends an email to a real user",
    "create_calendar_invite": "creates a calendar event",
    "approve_payment": "approves or spends money",
    "delete_file": "removes files permanently"
}

SPAM_WORDS = {
    "win", "prize", "reward", "cash", "compromised",
    "refund", "urgent", "congratulations",
    "lottery", "claim", "certificate"
}

PROMO_WORDS = {
    "discount", "offer", "sale", "deal", "free", "%",
    "voucher", "coupon", "buy", "save",
    "limited time", "subscribe", "unsubscribe", "newsletter"
}

ACTION_WORDS = {
    "schedule", "meeting", "call", "book", "approve",
    "send", "resolve", "review", "confirm",
    "sign", "assign", "complete", "follow up", "follow-up"
}

NORMAL_WORDS = {
    "hi", "hello", "regards", "thanks",
    "thank you", "best", "cheers", "team",
    "colleague", "attached"
}

DATE_TIME_WORDS = {
    "today", "tomorrow", "next", "monday", "tuesday",
    "wednesday", "thursday", "friday", "saturday",
    "sunday", "am", "pm", "deadline", "asap", "soon"
}

MODAL_REQUESTS = {
    "please", "could you", "can you",
    "would you", "let me know", "let us know"
}

def _count_hits(text, words):
    return sum(1 for w in words if w in text)

def _has_url(text):
    return bool(re.search(r"https?://|www\.", text))

def _currency_signs(text):
    return bool(re.search(r"[$€£¥]|usd|eur|gbp", text))

def _uppercase_ratio(text):
    letters = re.findall(r"[A-Za-z]", text)
    if not letters:
        return 0.0
    return sum(1 for c in letters if c.isupper()) / len(letters)

def rule_score(email_text):
    text = email_text.lower()
    scores = {k: 0.0 for k in LABELS}

    spam_hits = _count_hits(text, SPAM_WORDS)
    promo_hits = _count_hits(text, PROMO_WORDS)
    action_hits = _count_hits(text, ACTION_WORDS)
    normal_hits = _count_hits(text, NORMAL_WORDS)
    date_hits = _count_hits(text, DATE_TIME_WORDS)
    modal_hits = _count_hits(text, MODAL_REQUESTS)

    if _has_url(text):
        scores["spam"] += 1.5
        scores["promotion"] += 1.0

    if _currency_signs(text):
        scores["spam"] += 1.2

    if _uppercase_ratio(email_text) > 0.5:
        scores["spam"] += 1.5

    scores["spam"] += spam_hits * 2.0
    scores["promotion"] += promo_hits * 2.0
    scores["action_intent"] += action_hits * 2.5
    scores["action_intent"] += modal_hits * 1.5
    scores["action_intent"] += date_hits * 1.0
    scores["normal"] += normal_hits * 1.5

    return scores

def canonicalize_label(label):
    if not label:
        return "unknown"
    s = label.lower()
    if "spam" in s:
        return "spam"
    if "promo" in s or "sale" in s or "offer" in s:
        return "promotion"
    if "action" in s or "meeting" in s or "call" in s:
        return "action_intent"
    if "normal" in s or "personal" in s:
        return "normal"
    return "unknown"

def llm_fallback(email_text):
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f"Classify this email as spam, promotion, normal, or action_intent:\n{email_text}"
            }],
            max_tokens=10
        )
        return canonicalize_label(res.choices[0].message.content)
    except Exception:
        return "normal"

def triage_email(email_text):
    scores = rule_score(email_text)
    best = max(scores, key=scores.get)
    second = sorted(scores.values(), reverse=True)[1]

    if scores[best] >= 3.0 and (scores[best] - second) >= 1.5:
        return best

    return llm_fallback(email_text)

class TriageState(TypedDict):
    email_text: str
    label: str
    dangerous: bool

def action_node(state: TriageState) -> TriageState:
    email = state["email_text"]
    label = triage_email(email)

    return {
        "email_text": email,
        "label": label,
        "dangerous": label == "action_intent"
    }

workflow = StateGraph(TriageState)
workflow.add_node("action_node", action_node)
workflow.set_entry_point("action_node")
workflow.add_edge("action_node", END)

checkpointer = MemorySaver()

graph = workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["action_node"]
)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "milestone3"}}

    input_state = {
        "email_text": "Hi team, can we schedule a call tomorrow at 3pm?"
    }

    print("Paused before action")
    graph.invoke(input_state, config=config)

    print("Resuming after approval")
    result = graph.invoke(None, config=config)
    print(result)