import re
from openai import OpenAI

client = OpenAI()

LABELS = ["spam", "promotion", "normal", "action_intent", "unknown"]

# expanded lexicons
SPAM_WORDS = {"win", "prize", "reward", "cash", "compromised", "refund", "urgent", "congratulations", "lottery", "claim", "certificate"}
PROMO_WORDS = {"discount", "offer", "sale", "deal", "free", "%", "voucher", "coupon", "buy", "save", "limited time", "subscribe", "unsubscribe", "newsletter"}
ACTION_WORDS = {"schedule", "meeting", "call", "book", "approve", "send", "resolve", "review", "confirm", "sign", "assign", "complete", "follow up", "follow-up"}
NORMAL_WORDS = {"hi", "hello", "regards", "thanks", "thank you", "best", "cheers", "team", "colleague", "attached"}

DATE_TIME_WORDS = {"today", "tomorrow", "next", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "am", "pm", "deadline", "urgent", "asap", "soon"}
MODAL_REQUESTS = {"please", "could you", "can you", "would you", "let me know", "let us know", "would you please"}

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

def rule_score(email_text):
    text = email_text.lower()
    scores = {k: 0.0 for k in LABELS}

    # basic lexical hits
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

    # spam scoring
    scores["spam"] += spam_hits * 2.0
    if url:
        scores["spam"] += 1.5
    if currency:
        scores["spam"] += 1.2
    if upper_ratio > 0.5:
        scores["spam"] += 1.5
    scores["spam"] += min(exclaim, 3) * 0.5

    # promotion scoring
    scores["promotion"] += promo_hits * 2.0
    if pct:
        scores["promotion"] += 1.5
    if url:
        scores["promotion"] += 1.0
    if "unsubscribe" in text or "newsletter" in text:
        scores["promotion"] += 2.0

    # action intent scoring
    scores["action_intent"] += action_hits * 2.5
    scores["action_intent"] += modal_hits * 1.5
    scores["action_intent"] += date_hits * 1.0
    # requests that include actions + dates/time strongly indicate action_intent
    if action_hits and (date_hits or modal_hits):
        scores["action_intent"] += 2.0

    # normal scoring (conversational/personal)
    scores["normal"] += normal_hits * 1.5
    # penalize normal if spam/promo signals present
    scores["normal"] -= (spam_hits + promo_hits) * 0.7

    # ensure non-negative
    for k in scores:
        if scores[k] < 0:
            scores[k] = 0.0

    return scores

def canonicalize_label(label):
    if not label or not isinstance(label, str):
        return "unknown"
    s = label.lower()
    if "spam" in s:
        return "spam"
    if "promotion" in s or "promo" in s or "advert" in s or "sale" in s or "offer" in s:
        return "promotion"
    if "action" in s or "intent" in s or "task" in s or "meeting" in s or "call" in s or "approve" in s:
        return "action_intent"
    if "normal" in s or "inbox" in s or "personal" in s:
        return "normal"
    if "unknown" in s:
        return "unknown"
    # fallback attempts
    if "yes" in s or "no" in s:
        return "normal"
    return "unknown"

def llm_fallback(email_text):
    prompt = f"Classify this single-label into exactly one of: spam, promotion, normal, action_intent.\nEmail: {email_text}\nOnly return one label (spam|promotion|normal|action_intent)."
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )
        raw = res.choices[0].message.content.strip().lower()
        return canonicalize_label(raw)
    except Exception:
        # on any LLM error, prefer "normal" as safe default
        return "normal"

def triage_email(email_text):
    if not isinstance(email_text, str) or not email_text.strip():
        return "unknown"

    scores = rule_score(email_text)
    # pick best and second-best
    best_label = max(scores, key=scores.get)
    best_score = scores[best_label]
    second_score = max(v for k, v in scores.items() if k != best_label)

    # heuristic thresholds
    # if rules give strong signal, use it
    if best_score >= 3.0 and (best_score - second_score) >= 1.5:
        return best_label

    # if there is any reasonable signal (>=2.0) prefer rule but still consult LLM if ambiguous
    if best_score >= 2.0 and (best_score - second_score) >= 0.8:
        return best_label

    # otherwise ask the LLM (fallback) for difficult/ambiguous cases
    llm_label = llm_fallback(email_text)
    if llm_label in LABELS:
        return llm_label
    return "unknown"

if __name__ == "__main__":
    # demo / test code — must be indented under the if
    test_email = "Hi team,\nCan we schedule a call tomorrow at 3pm to review the Q4 budget? Thanks!"
    print(triage_email(test_email))