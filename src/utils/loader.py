from pathlib import Path
import json
from typing import List, Dict, Optional


BASE_DIR = Path(__file__).resolve().parents[2]  # project root
DATA_DIR = BASE_DIR / "data"


def load_email_from_txt(path: str | Path) -> str:
    """
    Load a single email from a .txt file.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Email file not found: {path}")
    return path.read_text(encoding="utf-8")


def load_emails_from_json(
    filename: str = "hf_emails.json", limit: Optional[int] = None
) -> List[Dict]:
    """
    Load a JSON file with format:
    [
      {"email": "...", "label": "ignore|notify_human|respond", ...},
      ...
    ]
    Located by default in the /data directory.
    """
    json_path = DATA_DIR / filename
    if not json_path.is_file():
        raise FileNotFoundError(f"Dataset file not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if limit is not None:
        data = data[:limit]

    return data


def ensure_data_dir() -> Path:
    """
    Ensure that the /data directory exists.
    Useful if you want to save generated datasets.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR
