import re
from typing import TypedDict
from openai import OpenAI

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# -------------------- LLM CLIENT --------------------
client = OpenAI()

# -------------------- LABELS --------------------
LABELS = ["spam", "promotion", "normal", "action_intent", "unknown"]

# -------------------- LEXICONS --------------------
SPAM_WORDS = {
    "win", "prize", "reward", "cash", "compromised", "refund",
    "urgent", "congratulations", "lottery", "claim", "certificate"
}

PROMO_WORDS = {
    "discount", "offer", "sale", "deal", "free", "%", "voucher",
    "coupon", "buy", "save", "limited time", "subscribe",
    "unsubscribe", "newsletter"
}

ACTION_WORDS = {
    "schedule", "meeting", "call", "book", "approve", "send",
    "resolve", "review", "confirm", "sign", "assign", "complete",
    "follow up", "follow-up"
}

NORMAL_WORDS = {
    "hi", "hello", "regards", "thanks", "thank you",
    "best", "cheers", "team", "colleague", "attached"
}

DATE_TIME_WORDS = {
    "today", "tomorrow", "next", "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "sunday",
    "am", "pm", "deadline", "urgent", "asap", "soon"
}

MODAL_REQUESTS = {
    "please", "could you", "can you", "would you",
    "let me know", "let us know", "would you please"
}

# -------------------- HELPERS --------------------
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
    upper = sum(1 for c in letters if c.isupper())
    return upper / len(letters)

# -------------------- RULE SCORING --------------------
def rule_score(email_text):
    text = email_text.lower()
    scores = {k: 0.0 for k in LABELS}

    spam_hits = _count_hits(text, SPAM_WORDS)
    promo_hits = _count_hits(text, PROMO_WORDS)
    action_hits = _count_hits(text, ACTION_WORDS)
    normal_hits = _count_hits(text, NORMAL_WORDS)
    date_hits = _count_hits(text, DATE_TIME_WORDS)
    modal_hits = _count_hits(text, MODAL_REQUESTS)

    url = _has_url(text)
    currency = _currency_signs(text)
    pct = "%" in text or re.search(r"\b\d+%|\bpercent\b", text)
    exclaim = text.count("!")
    upper_ratio = _uppercase_ratio(email_text)

    scores["spam"] += spam_hits * 2.0
    if url:
        scores["spam"] += 1.5
    if currency:
        scores["spam"] += 1.2
    if upper_ratio > 0.5:
        scores["spam"] += 1.5
    scores["spam"] += min(exclaim, 3) * 0.5

    scores["promotion"] += promo_hits * 2.0
    if pct:
        scores["promotion"] += 1.5
    if url:
        scores["promotion"] += 1.0
    if "unsubscribe" in text or "newsletter" in text:
        scores["promotion"] += 2.0

    scores["action_intent"] += action_hits * 2.5
    scores["action_intent"] += modal_hits * 1.5
    scores["action_intent"] += date_hits * 1.0
    if action_hits and (date_hits or modal_hits):
        scores["action_intent"] += 2.0

    scores["normal"] += normal_hits * 1.5
    scores["normal"] -= (spam_hits + promo_hits) * 0.7

    for k in scores:
        scores[k] = max(scores[k], 0.0)

    return scores

# -------------------- LABEL NORMALIZATION --------------------
def canonicalize_label(label):
    if not label or not isinstance(label, str):
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

# -------------------- LLM FALLBACK --------------------
def llm_fallback(email_text):
    prompt = (
        "Classify this email into exactly one label:\n"
        "spam, promotion, normal, action_intent\n\n"
        f"Email:\n{email_text}\n\n"
        "Return only the label."
    )
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )
        return canonicalize_label(res.choices[0].message.content.strip())
    except Exception:
        return "normal"

# -------------------- CORE TRIAGE LOGIC --------------------
def triage_email(email_text):
    if not isinstance(email_text, str) or not email_text.strip():
        return "unknown"

    scores = rule_score(email_text)
    best = max(scores, key=scores.get)
    best_score = scores[best]
    second = max(v for k, v in scores.items() if k != best)

    if best_score >= 3.0 and (best_score - second) >= 1.5:
        return best

    if best_score >= 2.0 and (best_score - second) >= 0.8:
        return best

    return llm_fallback(email_text)

# ==================== LANGGRAPH PART (MILESTONE 3) ====================

class TriageState(TypedDict):
    email_text: str
    label: str

def action_node(state: TriageState) -> TriageState:
    email = state["email_text"]
    label = triage_email(email)
    return {
        "email_text": email,
        "label": label
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

# -------------------- RUN + RESUME --------------------
if __name__ == "__main__":
    config = {
        "configurable": {
            "thread_id": "triage-hitl-1"
        }
    }

    input_state = {
        "email_text": "Hi team, can we schedule a call tomorrow at 3pm?"
    }

    print("⏸ First run (paused before action node)")
    graph.invoke(input_state, config=config)

    print("▶️ Resuming from checkpoint")
    result = graph.invoke(None, config=config)
    print(result)
        