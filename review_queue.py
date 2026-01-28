import json
import os
from typing import Any, Dict, List

from config import REVIEW_DB


def _ensure_db_exists():
    os.makedirs(os.path.dirname(REVIEW_DB), exist_ok=True)
    if not os.path.exists(REVIEW_DB):
        with open(REVIEW_DB, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_reviews() -> List[Dict[str, Any]]:
    _ensure_db_exists()
    try:
        with open(REVIEW_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_for_review(entry: Dict[str, Any]) -> None:
    _ensure_db_exists()
    data = load_reviews()
    data.append(entry)
    with open(REVIEW_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_reviewed_email(entry: Dict[str, Any]) -> None:
    """Append approved reviewed emails to reports/approved_actions.json."""
    reports_dir = os.path.join("reports")
    os.makedirs(reports_dir, exist_ok=True)
    approved_path = os.path.join(reports_dir, "approved_actions.json")

    approved: List[Dict[str, Any]] = []
    if os.path.exists(approved_path):
        try:
            with open(approved_path, "r", encoding="utf-8") as f:
                approved = json.load(f) or []
        except Exception:
            approved = []

    approved.append(entry)
    with open(approved_path, "w", encoding="utf-8") as f:
        json.dump(approved, f, indent=4)

def add_to_review_queue(entry: Dict[str, Any]) -> None:
    """Add an email entry to the review queue."""
    save_for_review(entry)