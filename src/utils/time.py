# src/utils/time.py
from datetime import datetime
from zoneinfo import ZoneInfo

USER_TZ = ZoneInfo("Asia/Kolkata")

def now_local():
    return datetime.now(USER_TZ)
