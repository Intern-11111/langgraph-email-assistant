import time
from collections import defaultdict
from threading import Lock

# Max API calls per minute per tool
RATE_LIMITS = {
    "send_email": 30,
    "create_calendar_event": 20,
}

_call_counts = defaultdict(int)
_last_reset = defaultdict(float)
_lock = Lock()


def enforce_rate_limit(tool_name: str):
    """
    Blocks execution if rate limit exceeded.
    """

    limit = RATE_LIMITS.get(tool_name)
    if not limit:
        return  # No limit defined

    now = time.time()

    with _lock:
        # Reset every 60 seconds
        if now - _last_reset[tool_name] > 60:
            _call_counts[tool_name] = 0
            _last_reset[tool_name] = now

        if _call_counts[tool_name] >= limit:
            raise RuntimeError(
                f"Rate limit exceeded for tool: {tool_name}"
            )

        _call_counts[tool_name] += 1
