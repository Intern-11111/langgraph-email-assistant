import argparse
import json
import os
from typing import Any, Dict, List, Optional


def load_events(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_events(path: str, events: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)


def select_record(
    events: List[Dict[str, Any]],
    index: Optional[int] = None,
    tool: Optional[str] = None,
    title: Optional[str] = None,
) -> Optional[int]:
    """
    Return the index of the selected record.
    Priority: explicit index > last matching by (tool/title) > None
    """
    if not events:
        return None
    if index is not None:
        if 0 <= index < len(events):
            return index
        return None
    # filter by tool/title and pick the last match
    candidates = list(range(len(events)))
    if tool:
        candidates = [i for i in candidates if events[i].get("tool") == tool]
    if title:
        candidates = [
            i
            for i in candidates
            if (events[i].get("event", {}).get("title") == title)
        ]
    if candidates:
        return candidates[-1]
    return None


def merge_event_fields(record: Dict[str, Any], update: Dict[str, Any]) -> None:
    """
    Shallow-merge fields for event records or email_status records.
    - If tool == create_event: update "event" dict keys
    - If tool == email_status: update top-level keys (e.g., status) and nested "final" dict
    """
    tool = record.get("tool")
    if tool == "create_event":
        event = record.get("event", {})
        if not isinstance(event, dict):
            event = {}
        # Only merge into event sub-structure
        event.update({k: v for k, v in update.items()})
        record["event"] = event
    elif tool == "email_status":
        # Merge top-level primitives (e.g., status)
        for k, v in update.items():
            if k == "final" and isinstance(v, dict):
                final = record.get("final", {})
                if not isinstance(final, dict):
                    final = {}
                final.update(v)
                record["final"] = final
            else:
                record[k] = v
    else:
        # Unknown tool: apply shallow merge at top level
        for k, v in update.items():
            record[k] = v


def update_user_events(
    store_path: str,
    index: Optional[int] = None,
    tool: Optional[str] = None,
    title: Optional[str] = None,
    update_json: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    events = load_events(store_path)
    if not events:
        return {"updated": False, "reason": "No events found", "path": store_path}
    target_idx = select_record(events, index=index, tool=tool, title=title)
    if target_idx is None:
        return {
            "updated": False,
            "reason": "No matching record",
            "path": store_path,
        }
    record = events[target_idx]
    if update_json:
        merge_event_fields(record, update_json)
        events[target_idx] = record
        save_events(store_path, events)
        return {
            "updated": True,
            "index": target_idx,
            "tool": record.get("tool"),
            "path": store_path,
        }
    else:
        return {"updated": False, "reason": "No update_json provided"}


def _parse_update_json(raw: Optional[str]) -> Optional[Dict[str, Any]]:
    if not raw:
        return None
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Update portions of data/user_events.json")
    parser.add_argument(
        "--path",
        default=os.path.join("data", "user_events.json"),
        help="Path to user_events.json",
    )
    parser.add_argument(
        "--index",
        type=int,
        help="Explicit index of record to update (0-based)",
    )
    parser.add_argument(
        "--tool",
        help="Filter by tool type (e.g., create_event, email_status)",
    )
    parser.add_argument(
        "--title",
        help="Filter by event title (for create_event records)",
    )
    parser.add_argument(
        "--update-json",
        help="JSON object to merge. For create_event: merged into 'event'. For email_status: merged into top-level and 'final' if provided.",
    )
    parser.add_argument(
        "--update-file",
        help="Path to a JSON file containing the update object (avoids shell quoting issues)",
    )

    args = parser.parse_args()
    update_obj = _parse_update_json(args.update_json)
    if not update_obj and args.update_file:
        try:
            with open(args.update_file, "r", encoding="utf-8") as f:
                raw = f.read()
            update_obj = _parse_update_json(raw)
        except Exception:
            update_obj = None
    result = update_user_events(
        store_path=args.path,
        index=args.index,
        tool=args.tool,
        title=args.title,
        update_json=update_obj,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
